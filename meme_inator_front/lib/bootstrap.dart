// ignore_for_file: omit_local_variable_types

import 'dart:async';
import 'dart:developer';

import 'package:bloc/bloc.dart';
import 'package:flutter/widgets.dart';
import 'package:get_it/get_it.dart';
import 'package:logging/logging.dart';
import 'package:meme_inator_front/app/app_sl_injector.dart';
import 'package:meme_inator_front/core/observers/bloc_observer.dart';


/// I created custom AppBlocObserver in /core/observers/bloc_observer.dart
/// TODO: Get rid of this. 
// class AppBlocObserver extends BlocObserver {
//   const AppBlocObserver();

//   @override
//   void onChange(BlocBase<dynamic> bloc, Change<dynamic> change) {
//     super.onChange(bloc, change);
//     log('onChange(${bloc.runtimeType}, $change)');
//   }

//   @override
//   void onError(BlocBase<dynamic> bloc, Object error, StackTrace stackTrace) {
//     log('onError(${bloc.runtimeType}, $error, $stackTrace)');
//     super.onError(bloc, error, stackTrace);
//   }
// }

/// Bootstrap initializes constructs that are in ALL flavors (production, staging, deveopment)
/// if construct specific to a flavor, initalize it in its specific main_.dart
/// Bootstrap initializes envionrment, configuration, and dependencies
/// for memeinator. 
Future<void> bootstrap(FutureOr<Widget> Function() builder) async {
  FlutterError.onError = (details) {
    log(details.exceptionAsString(), stackTrace: details.stack);
  };

  // Add cross-flavor configuration here
  // ... Initialize GetIt
  final GetIt serviceLocator = GetIt.instance;
  await configureAppServiceLocatorDependencies(serviceLocator);

  // ... Setup logger
  Logger.root.level = Level.ALL;
  Logger.root.onRecord.listen((record) {
    debugPrint('${record.level.name}: ${record.time}: ${record.message}');
  });

  Bloc.observer = AppBlocObserver();
  runApp(await builder());
}
