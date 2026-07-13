// lib/features/users/users_injector.dart
// ignore_for_file: cascade_invocations

import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/users/data/models/repositories/user_repository_imp.dart';
import 'package:meme_inator_front/features/users/data/models/services/user_api_service.dart';
import 'package:meme_inator_front/features/users/domain/interfaces/iuser_repository.dart';
import 'package:meme_inator_front/features/users/domain/usecases/followship_usecases/follow_user_usecase.dart';
import 'package:meme_inator_front/features/users/domain/usecases/followship_usecases/unfollow_user_usecase.dart';
import 'package:meme_inator_front/features/users/domain/usecases/get_current_user_usecase.dart';

void configureUsersDependencies(GetIt sl) {
  sl.registerLazySingleton<UserApiService>(() => UserApiService(sl<Dio>()));
  sl.registerLazySingleton<IUserRepository>(() => UserRepositoryImpl(sl<UserApiService>()));
  sl.registerLazySingleton<FollowUserUsecase>(() => FollowUserUsecase(sl<IUserRepository>()));
  sl.registerLazySingleton<UnfollowUserUsecase>(() => UnfollowUserUsecase(sl<IUserRepository>()));
  sl.registerLazySingleton<GetCurrentUserUsecase>(() => GetCurrentUserUsecase(sl<IUserRepository>()));
}
