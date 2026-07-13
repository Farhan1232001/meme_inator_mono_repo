// lib/features/profiles/profiles_injector.dart
// ignore_for_file: cascade_invocations

import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/profiles/data/models/repositories/profile_repository_impl.dart';
import 'package:meme_inator_front/features/profiles/data/models/services/profile_api_service.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/create_user_profile_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_my_profile_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_profile_img_urls_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_profile_posts_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_public_profile_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_public_profile_with_followship_uc.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/patch_my_profile_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/profile_entity_from_repository_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/replace_my_profile_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/sync_profile_media_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/update_profile_counters_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/validate_profile_usecase.dart';

void configureProfilesDependencies(GetIt sl) {
  // API Service
  sl.registerLazySingleton<ProfileApiService>(
    () => ProfileApiService(sl<Dio>()),
  );
  
  // Repository
  sl.registerLazySingleton<IProfileRepository>(
    () => ProfileRepositoryImpl(sl<ProfileApiService>()),
  );
  
  // ==================== PUBLIC PROFILE USECASES ====================

  sl.registerLazySingleton<GetPublicProfileWithFollowshipUsecase>(
    () => GetPublicProfileWithFollowshipUsecase(repository: sl<IProfileRepository>()),
  );
  
  /// Get public profile by username
  sl.registerLazySingleton<GetPublicProfileUsecase>(
    () => GetPublicProfileUsecase(repository: sl<IProfileRepository>()),
  );
  
  /// Get profile posts for a user
  sl.registerLazySingleton<GetProfilePostsUsecase>(
    () => GetProfilePostsUsecase(repository: sl<IProfileRepository>()),
  );
  
  // ==================== OWN PROFILE USECASES ====================
  
  /// Get current user's own profile
  sl.registerLazySingleton<GetMyProfileUsecase>(
    () => GetMyProfileUsecase(repository: sl<IProfileRepository>()),
  );
  
  /// Create a new profile for the current user
  sl.registerLazySingleton<CreateUserProfileUsecase>(
    () => CreateUserProfileUsecase(sl<IProfileRepository>()),
  );
  
  /// Partially update current user's profile
  sl.registerLazySingleton<PatchMyProfileUsecase>(
    () => PatchMyProfileUsecase(sl<IProfileRepository>()),
  );
  
  /// Fully replace current user's profile
  sl.registerLazySingleton<ReplaceMyProfileUsecase>(
    () => ReplaceMyProfileUsecase(sl<IProfileRepository>()),
  );
  
  // ==================== COUNTERS & MEDIA ====================
  
  /// Update profile counters (likes, followers, etc.)
  sl.registerLazySingleton<UpdateProfileCountersUsecase>(
    () => UpdateProfileCountersUsecase(sl<IProfileRepository>()),
  );
  
  /// Sync media after upload (profile pic, header, etc.)
  sl.registerLazySingleton<SyncProfileMediaUsecase>(
    () => SyncProfileMediaUsecase(sl<IProfileRepository>()),
  );
  
  /// Get profile image URLs (presigned)
  sl.registerLazySingleton<GetProfileImageUrlsUsecase>(
    () => GetProfileImageUrlsUsecase(sl<IProfileRepository>()),
  );
  
  // ==================== VALIDATION & UTILITY ====================
  
  /// Validate profile data before sending
  sl.registerLazySingleton<ValidateProfileUsecase>(
    () => ValidateProfileUsecase(sl<IProfileRepository>()),
  );
  
  /// Convert raw repository data to ProfileEntity
  sl.registerLazySingleton<ProfileEntityFromRepositoryUsecase>(
    () => ProfileEntityFromRepositoryUsecase(sl<IProfileRepository>()),
  );
}
