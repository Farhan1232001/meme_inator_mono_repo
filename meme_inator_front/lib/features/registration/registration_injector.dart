// ignore_for_file: cascade_invocations

import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/registration/data/models/repositories/registration_repository_impl.dart';
import 'package:meme_inator_front/features/registration/data/models/services/registration_api_service.dart';
import 'package:meme_inator_front/features/registration/domain/repositories/iregistration_repo.dart';
import 'package:meme_inator_front/features/registration/domain/usecases/confirm_deregistration_usecase.dart';
import 'package:meme_inator_front/features/registration/domain/usecases/deregister_usecase.dart';
import 'package:meme_inator_front/features/registration/domain/usecases/register_usecase.dart';
import 'package:meme_inator_front/features/registration/domain/usecases/verify_registration_usecase.dart';

// Update the existing empty auth_injector.dart
void configureRegistrationDependencies(GetIt sl) {

  // API Service - Requires Dio to be registered in core module
  sl.registerLazySingleton<RegistrationApiService>(
    () => RegistrationApiService(sl<Dio>()),
  );
  // Repository
  sl.registerLazySingleton<IRegistrationRepository>(
    () => RegistrationRepositoryImpl(
      sl<RegistrationApiService>(),
    ),
  );
  
  // Use Cases
  sl.registerLazySingleton<RegisterUsecase>(
    () => RegisterUsecase(sl<IRegistrationRepository>()),
  );
  
  sl.registerLazySingleton<VerifyRegistrationUsecase>(
    () => VerifyRegistrationUsecase(sl<IRegistrationRepository>()),
  );
  
  sl.registerLazySingleton<DeregisterUsecase>(
    () => DeregisterUsecase(sl<IRegistrationRepository>()),
  );
  
  sl.registerLazySingleton<ConfirmDeregistrationUsecase>(
    () => ConfirmDeregistrationUsecase(sl<IRegistrationRepository>()),
  );
}
