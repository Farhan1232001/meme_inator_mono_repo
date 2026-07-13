// ignore_for_file: cascade_invocations

import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/auth/data/models/repositories/auth_repository_impl.dart';
import 'package:meme_inator_front/features/auth/data/models/services/auth_api_service.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';
import 'package:meme_inator_front/features/auth/domain/services/itoken_storage_service.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/check_login_status_usecase.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/clear_token_pair_usecase.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/get_current_user_from_token_usecase.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/get_stored_token_pair_uc.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/login_usecase.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/logout_usecase.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/refresh_tokens_usecase.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/save_token_pair_usecase.dart';
import 'package:meme_inator_front/features/users/domain/usecases/get_current_user_usecase.dart';

// Update the existing empty auth_injector.dart
void configureAuthDependencies(GetIt sl) {

  // API Service - Requires Dio to be registered in core module
  sl.registerLazySingleton<AuthApiService>(
    () => AuthApiService(sl<Dio>()),
  );
  // Repository
  sl.registerLazySingleton<IAuthRepository>(
    () => AuthRepositoryImpl(
      sl<AuthApiService>(),
      sl<ITokenStorageService>(),
    ),
  );
  
  // Use Cases
  sl.registerLazySingleton<LoginUsecase>(
    () => LoginUsecase(sl<IAuthRepository>()),
  );
  
  sl.registerLazySingleton<LogoutUsecase>(
    () => LogoutUsecase(sl<IAuthRepository>()),
  );
  
  sl.registerLazySingleton<RefreshTokenUsecase>(
    () => RefreshTokenUsecase(sl<IAuthRepository>()),
  );
  
  // sl.registerLazySingleton<GetCurrentUserUsecase>(
  //   () => GetCurrentUserUsecase(sl<IAuthRepository>()),
  // );
  sl.registerLazySingleton<GetCurrentUserFromTokenUsecase>(
    () => GetCurrentUserFromTokenUsecase(sl<IAuthRepository>()),
  );
  
  sl.registerLazySingleton<CheckLoginStatusUsecase>(
    () => CheckLoginStatusUsecase(sl<IAuthRepository>()),
  );
  
  sl.registerLazySingleton<GetStoredTokenPairUsecase>(
    () => GetStoredTokenPairUsecase(sl<IAuthRepository>()),
  );
  
  sl.registerLazySingleton<SaveTokenPairUsecase>(
    () => SaveTokenPairUsecase(sl<IAuthRepository>()),
  );
  
  sl.registerLazySingleton<ClearTokenPairUsecase>(
    () => ClearTokenPairUsecase(sl<IAuthRepository>()),
  );
}
