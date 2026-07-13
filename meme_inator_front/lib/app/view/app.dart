// ignore_for_file: lines_longer_than_80_chars
// lib/app/view/app.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:meme_inator_front/app/app_bloc_providers.dart';
import 'package:meme_inator_front/app/app_router.dart';
import 'package:meme_inator_front/app/app_theme.dart';
import 'package:meme_inator_front/l10n/gen/app_localizations.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {

    return PlatformProvider(
      builder: (context) => PlatformTheme(
        themeMode: ThemeMode.system,
        materialLightTheme: AppTheme.materialLightTheme,
        materialDarkTheme: AppTheme.materialDarkTheme,
        cupertinoLightTheme: AppTheme.cupertinoLightTheme,
        cupertinoDarkTheme: AppTheme.cupertinoDarkTheme,
        // PlatformApp.router to be wrapped with 
        // "MultiBlocProvider(providers: global_bloc_providers,child: etc"
        builder: (context) => MultiBlocProvider(
          providers: globalBlocProviders,
          child: PlatformApp.router(
            debugShowCheckedModeBanner: false,
            title: 'Meme-inator',
            localizationsDelegates: AppLocalizations.localizationsDelegates,
            supportedLocales: AppLocalizations.supportedLocales,
            routerConfig: appRouter, // Use routerConfig for GoRouter 7+
          ),
        ),
      ),
    );
  }
}
