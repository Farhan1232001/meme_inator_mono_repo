// lib/features/users/data/repositories/user_repository_impl.dart
import 'package:dio/dio.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/users/data/models/services/user_api_service.dart';
import 'package:meme_inator_front/features/users/domain/entities/user_entity.dart';
import 'package:meme_inator_front/features/users/domain/interfaces/iuser_repository.dart';
import 'package:meme_inator_front/features/users/users_mappers.dart';

class UserRepositoryImpl implements IUserRepository {
  final UserApiService _apiService;

  UserRepositoryImpl(this._apiService);

  @override
  Future<Result<void>> followUser(String userId) async {
    try {
      await _apiService.followUser(userId);
      return const Ok(null);
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception);
    }
  }

  @override
  Future<Result<void>> unfollowUser(String userId) async {
    try {
      await _apiService.unfollowUser(userId);
      return const Ok(null);
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception);
    }
  }

  @override
  Future<Result<UserEntity>> getCurrentUser() async {
    try {
      final dto = await _apiService.getUserByToken();
      return Ok(UsersMapper.dtoToEntity(dto));
    } on DioException catch (e) {
      return _handleError(e);
    } catch (e) {
      return Error.fromException(e as Exception);
    }
  }

  Result<T> _handleError<T>(DioException e) {
    // similar to profile repository error handling
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
