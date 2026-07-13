import 'package:dio/dio.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/data/dtos/counters_update_dto.dart';
import 'package:meme_inator_front/features/profiles/data/dtos/media_sync_dto.dart';
import 'package:meme_inator_front/features/profiles/data/dtos/update_profile_request_dto.dart';
import 'package:meme_inator_front/features/profiles/data/models/services/profile_api_service.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';
import 'package:meme_inator_front/features/profiles/profiles_mapper.dart';

class ProfileRepositoryImpl implements IProfileRepository {
  final ProfileApiService _apiService;

  ProfileRepositoryImpl(this._apiService);

  @override
  Future<Result<ProfileEntity>> getPublicProfileWithFollowshipContext({
    required String profileOwnerUserId,
    String? viewerUserId,
    List<String>? fields,
  }) async {
    try {
      final fieldsParam = fields?.join(',');
      final dto = await _apiService.getPublicProfileWithFollowshipContext(
        profileOwnerUserId,
        fieldsParam,
      );
      return Ok(ProfilesMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<ProfileEntity>> getPublicProfile({
    required String username,
    String? viewerUserId,
  }) async {
    try {
      final dto = await _apiService.getPublicProfile(
        username,
        viewerUserId: viewerUserId,
      );
      return Ok(ProfilesMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<ProfileEntity>> getMyProfile() async {
    try {
      final dto = await _apiService.getMyProfile();
      return Ok(ProfilesMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<ProfileEntity>> createProfile() async {
    try {
      final dto = await _apiService.createProfile();
      return Ok(ProfilesMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<ProfileEntity>> patchMyProfile(
    Map<String, dynamic> partialData,
  ) async {
    try {
      final request = UpdateProfileRequestDto.fromJson(partialData);
      final dto = await _apiService.patchMyProfile(request);
      return Ok(ProfilesMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<ProfileEntity>> replaceMyProfile(
    Map<String, dynamic> fullData,
  ) async {
    try {
      final request = UpdateProfileRequestDto.fromJson(fullData);
      final dto = await _apiService.replaceMyProfile(request);
      return Ok(ProfilesMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<ProfileEntity>> updateCounters(
    Map<String, int> increments,
  ) async {
    try {
      final request = CountersUpdateDto(increments: increments);
      final dto = await _apiService.updateCounters(request);
      return Ok(ProfilesMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<ProfileEntity>> syncMedia(
    Map<String, dynamic> mediaPayload,
  ) async {
    try {
      final request = MediaSyncDto.fromJson(mediaPayload);
      final dto = await _apiService.syncMedia(request);
      return Ok(ProfilesMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<Map<String, dynamic>>> getProfilePosts({
    required String username,
    String? cursor,
    int pageSize = 10,
  }) async {
    try {
      final response = await _apiService.getProfilePosts(
        username,
        cursor: cursor,
        pageSize: pageSize,
      );
      return Ok(response);
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<Map<String, String>>> getProfileImageUrls() async {
    try {
      final response = await _apiService.getProfileImageUrls();
      return Ok(response);
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception, message: 'Unexpected error');
    }
  }

  @override
  Future<Result<void>> validateProfile(Map<String, dynamic> profileData) async {
    // Usually validation is done client-side; if backend validation needed, add endpoint.
    return const Ok(null);
  }

  Result<T> _handleError<T>(DioException e) {
    final statusCode = e.response?.statusCode;
    final message = e.response?.data?['message'] ?? e.message;
    if (statusCode == 404) {
      return NotOk.notFound(message: message as String);
    } else if (statusCode == 400) {
      return NotOk.badRequest(message: message as String);
    } else if (statusCode == 401) {
      return NotOk.unauthorized(message: message as String);
    } else {
      return Error.fromException(e, message: message as String);
    }
  }
}
