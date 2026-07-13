// lib/features/profiles/domain/interfaces/iprofile_repository.dart
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';

abstract class IProfileRepository {
  // Public profile
  Future<Result<ProfileEntity>> getPublicProfile({
    required String username,
    String? viewerUserId,
  });

  /// Fetch a public profile including whether the authenticated user follows it.
  /// [profileOwnerUserId] is the UUID of the profile being viewed.
  /// The viewer's ID is taken from the backend's auth context automatically.
  Future<Result<ProfileEntity>> getPublicProfileWithFollowshipContext({
    required String profileOwnerUserId,
    String? viewerUserId, // optional, backend extracts from token anyway
    List<String>? fields,
  });

  // Own profile
  Future<Result<ProfileEntity>> getMyProfile();
  Future<Result<ProfileEntity>> createProfile();
  Future<Result<ProfileEntity>> patchMyProfile(
    Map<String, dynamic> partialData,
  );
  Future<Result<ProfileEntity>> replaceMyProfile(Map<String, dynamic> fullData);

  // Counters
  Future<Result<ProfileEntity>> updateCounters(Map<String, int> increments);

  // Media sync
  Future<Result<ProfileEntity>> syncMedia(Map<String, dynamic> mediaPayload);

  // Posts - returns raw map that can be converted by usecase
  Future<Result<Map<String, dynamic>>> getProfilePosts({
    required String username,
    String? cursor,
    int pageSize = 10,
  });

  // Image URLs (presigned)
  Future<Result<Map<String, String>>> getProfileImageUrls();

  // Validation (optional – could be used before sending)
  Future<Result<void>> validateProfile(Map<String, dynamic> profileData);
}
