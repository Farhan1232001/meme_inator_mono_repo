// lib/injection_container.dart
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/core/core_injector.dart';
import 'package:meme_inator_front/features/auth/auth_injector.dart';
import 'package:meme_inator_front/features/feeds/feeds_sl_injector.dart';
import 'package:meme_inator_front/features/home/home_sl_injector.dart';
import 'package:meme_inator_front/features/profiles/profiles_sl_injector.dart';
import 'package:meme_inator_front/features/registration/registration_injector.dart';
import 'package:meme_inator_front/features/users/users_injector.dart';

/// Service locator initalized in bootstrap.dart
Future<void> configureAppServiceLocatorDependencies(GetIt sl) async {
  // Configure dependencies in correct order
  // ... Core
  configureCoreDependencies(sl);
  
  // ... Domain & Data Layer (Use GetIt for these)
  configureAuthDependencies(sl);
  configureFeedsDependencies(sl);
  configureProfilesDependencies(sl);
  configureHomeDependencies(sl);
  configureRegistrationDependencies(sl);
  configureUsersDependencies(sl);
  
  // ... UI Layer (USES app_bloc_providers.dart & Bloc related constructs)
}
