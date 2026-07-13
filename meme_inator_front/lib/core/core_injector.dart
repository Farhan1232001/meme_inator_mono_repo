// lib/core/core_injector.dart
// ignore_for_file: cascade_invocations

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/core/api/api_endpoints_base.dart';
import 'package:meme_inator_front/features/auth/data/auth_interceptor.dart';
import 'package:meme_inator_front/features/auth/data/models/services/secure_token_storage_service.dart';
import 'package:meme_inator_front/features/auth/domain/services/itoken_storage_service.dart';

void configureCoreDependencies(GetIt sl) {
  // External dependencies
  sl.registerLazySingleton<FlutterSecureStorage>(() => const FlutterSecureStorage());
  
  // ... Services
  sl.registerLazySingleton<ITokenStorageService>(
    () => SecureTokenStorage(sl<FlutterSecureStorage>()),
  );

  // ... Register Dio with proper configuration
  sl.registerLazySingleton<Dio>(() {
    final dio = Dio(BaseOptions(
      baseUrl: ApiEndpointsBase.getCurrentBaseUrl() + ApiEndpointsBase.apiPrefix,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      sendTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));
    
    // Add interceptors if you have them
    // dio.interceptors.add(LogInterceptor());
    dio.interceptors.add(AuthInterceptor(sl<ITokenStorageService>(), dio));
    
    return dio;
  });
  
  // Register other core dependencies here
  // sl.registerLazySingleton<StorageService>(() => StorageService());
  // sl.registerLazySingleton<AuthService>(() => AuthService());
}