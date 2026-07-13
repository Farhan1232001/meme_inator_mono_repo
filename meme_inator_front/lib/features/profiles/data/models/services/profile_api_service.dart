import 'package:dio/dio.dart';
import 'package:meme_inator_front/features/profiles/data/dtos/counters_update_dto.dart';
import 'package:meme_inator_front/features/profiles/data/dtos/media_sync_dto.dart';
import 'package:meme_inator_front/features/profiles/data/dtos/profile_response_dto.dart';
import 'package:meme_inator_front/features/profiles/data/dtos/update_profile_request_dto.dart';
import 'package:retrofit/retrofit.dart';

part 'profile_api_service.g.dart';

@RestApi()
abstract class ProfileApiService {
  factory ProfileApiService(Dio dio, {String baseUrl}) = _ProfileApiService;

  // Public profile

  @GET('/profiles/profile/{profile_owner_user_id}/with_followship_context')
  Future<ProfileResponseDto> getPublicProfileWithFollowshipContext(
    @Path('profile_owner_user_id') String username,
    @Query('fields') String? fields,
  );


  @GET('/profiles/{username}')
  Future<ProfileResponseDto> getPublicProfile(
    @Path('username') String username, {
    @Query('viewerUserId') String? viewerUserId,
  });

  // Own profile
  @GET('/profiles/me')
  Future<ProfileResponseDto> getMyProfile();

  @POST('/profiles/me')
  Future<ProfileResponseDto> createProfile();

  @PATCH('/profiles/me')
  Future<ProfileResponseDto> patchMyProfile(
    @Body() UpdateProfileRequestDto body,
  );

  @PUT('/profiles/me')
  Future<ProfileResponseDto> replaceMyProfile(
    @Body() UpdateProfileRequestDto body,
  );

  // Counters
  @PATCH('/profiles/me/counters')
  Future<ProfileResponseDto> updateCounters(
    @Body() CountersUpdateDto body,
  );

  // Media sync (after upload)
  @POST('/profiles/me/syncMedia')
  Future<ProfileResponseDto> syncMedia(
    @Body() MediaSyncDto body,
  );

  // Profile posts (separate feature, might be in posts service)
  @GET('/profiles/{username}/posts')
  Future<Map<String, dynamic>> getProfilePosts(
    @Path('username') String username, {
    @Query('cursor') String? cursor,
    @Query('page_size') int pageSize = 10,
  });

  // Image URLs (if needed separately)
  @GET('/profiles/me/images')
  Future<Map<String, String>> getProfileImageUrls();
}