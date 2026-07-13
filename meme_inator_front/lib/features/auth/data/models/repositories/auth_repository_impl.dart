// features/auth/data/models/repositories/auth_repository_impl.dart
import 'package:dio/dio.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/core/utils/jwt_decoder.dart';
import 'package:meme_inator_front/features/auth/data/dtos/login_request_dto.dart';
import 'package:meme_inator_front/features/auth/data/dtos/logout_request_dto.dart';
import 'package:meme_inator_front/features/auth/data/dtos/refresh_request_dto.dart';
import 'package:meme_inator_front/features/auth/data/models/services/auth_api_service.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';
import 'package:meme_inator_front/features/auth/domain/services/itoken_storage_service.dart';
import 'package:meme_inator_front/features/users/domain/entities/user_entity.dart';
import 'package:uuid/uuid_value.dart';

class AuthRepositoryImpl implements IAuthRepository {
  final AuthApiService _apiService;
  final ITokenStorageService _tokenStorageService;

  AuthRepositoryImpl(this._apiService, this._tokenStorageService);

  @override
  Future<Result<TokenPair>> login({
    required String usernameOrEmail,
    required String password,
    required bool rememberMe,
  }) async {
    try {
      final request = LoginRequestDto(
        usernameOrEmail: usernameOrEmail,
        password: password,
        rememberMe: rememberMe,
      );
      final response = await _apiService.login(request);
      final tokenPair = TokenPair(
        accessToken: response.access,
        refreshToken: response.refresh,
        expiresIn:
            3600, // TODO: default; actual value may come from backend. you could also parse from response if provided. make sure response returns an expiresIn and use it to make TokenPair
      );
      // Save tokens
      await _tokenStorageService.saveTokenPair(tokenPair);
      return Ok(tokenPair);
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        return NotOk.unauthorized(message: 'Invalid credentials');
      }
      return Error.fromException(e, message: 'Login failed');
    } catch (e) {
      return Error(
        message: 'Unexpected error during login',
        statusCode: -1,
        staticMessage: null,
        exception: e is Exception ? e : Exception(e.toString()),
      );
    }
  }

  @override
  Future<Result<void>> logout() async {
    try {
      final stored = await _tokenStorageService.getTokenPair();
      if (stored == null) return const Ok(null);

      final request = LogoutRequestDto(refresh: stored.refreshToken);
      await _apiService.logout(request);
      await _tokenStorageService.clearTokenPair();
      return const Ok(null);
    } on DioException catch (e) {
      // Even if logout fails on server, clear local tokens
      await _tokenStorageService.clearTokenPair();
      return Error.fromException(
        e,
        message: 'Logout failed, but local tokens cleared',
      );
    } catch (e) {
      await _tokenStorageService.clearTokenPair();
      return Error(
        message: 'Unexpected error during logout',
        statusCode: -1,
        staticMessage: null,
        exception: e is Exception ? e : Exception(e.toString()),
      );
    }
  }

  @override
  Future<Result<TokenPair>> refreshToken({required String refreshToken}) async {
    try {
      final request = RefreshRequestDto(refresh: refreshToken);
      final response = await _apiService.refresh(request);
      final newPair = TokenPair(
        accessToken: response.access,
        refreshToken: response.refresh,
        expiresIn: 3600,
      );
      await _tokenStorageService.saveTokenPair(newPair);
      return Ok(newPair);
    } on DioException catch (e) {
      if (e.response?.statusCode == 400 || e.response?.statusCode == 401) {
        // Refresh token invalid or expired → clear storage
        await _tokenStorageService.clearTokenPair();
        return NotOk.unauthorized(message: 'Refresh token expired');
      }
      return Error.fromException(e, message: 'Token refresh failed');
    } catch (e) {
      return Error(
        message: 'Unexpected error during token refresh',
        statusCode: -1,
        staticMessage: null,
        exception: e is Exception ? e : Exception(e.toString()),
      );
    }
  }

  @override
  Future<Result<UserEntity>> getCurrentUser() async {
    // First try to get access token
    final tokenPairResult = await getStoredTokenPair();

    return tokenPairResult.match(
      ok: (tokenPair) {
        if (tokenPair == null) {
          return NotOk.notFound(message: 'No token found');
        }

        // Try to get user_id from access token first
        String? userId = JwtUtils.getUserId(tokenPair.accessToken);

        // If not found in access token, try refresh token
        if (userId == null || userId.isEmpty) {
          userId = JwtUtils.getUserId(tokenPair.refreshToken);
        }

        // If still no user_id, return NotOk
        if (userId == null || userId.isEmpty) {
          return NotOk.notFound(message: 'User ID not found in tokens');
        }

        // Create UserEntity with the extracted user_id
        // Note: You might want to fetch full user details from an API endpoint
        // For now, create a basic UserEntity
        final user = UserEntity(
          id: UuidValue.fromString(userId),
          username: '',
          email: '',
          // You may want to add more fields if available from token
          // username: JwtUtils.getUsername(tokenPair.accessToken),
        );

        return Ok(user);
      },
      notOk: (notOk) => NotOk.notFound(message: notOk.message),
      error: (error) => Error(
        message: 'Failed to retrieve tokens: ${error.message}',
        statusCode: error.statusCode,
        staticMessage: error.staticMessage,
        exception: error.exception,
      ),
    );
  }

  @override
  Future<Result<String>> getCurrentUserViaToken(TokenPair? accessToken) async {
    if (accessToken != null) return _handleOkTokenPairResult(accessToken);

    // First try to get access token
    final tokenPairResult = await getStoredTokenPair();
    return tokenPairResult.match(
      ok: _handleOkTokenPairResult,
      notOk: (notOk) => NotOk.notFound(message: notOk.message),
      error: (error) => Error(
        message: 'Failed to retrieve tokens: ${error.message}',
        statusCode: error.statusCode,
        staticMessage: error.staticMessage,
        exception: error.exception,
      ),
    );
  }

  @override
  Future<Result<bool>> isLoggedIn() async {
    final token = await _tokenStorageService.getTokenPair();
    return Ok(token != null);
  }

  @override
  Future<Result<void>> saveTokenPair(TokenPair tokenPair) async {
    try {
      await _tokenStorageService.saveTokenPair(tokenPair);
      return const Ok(null);
    } catch (e) {
      return Error(
        message: 'Failed to save tokens',
        statusCode: -1,
        staticMessage: null,
        exception: e is Exception ? e : Exception(e.toString()),
      );
    }
  }

  @override
  Future<Result<TokenPair?>> getStoredTokenPair() async {
    try {
      final pair = await _tokenStorageService.getTokenPair();
      return Ok(pair);
    } catch (e) {
      return Error(
        message: 'Failed to read tokens',
        statusCode: -1,
        staticMessage: null,
        exception: e is Exception ? e : Exception(e.toString()),
      );
    }
  }

  @override
  Future<Result<void>> clearTokenPair() async {
    try {
      await _tokenStorageService.clearTokenPair();
      return const Ok(null);
    } catch (e) {
      return Error(
        message: 'Failed to clear tokens',
        statusCode: -1,
        staticMessage: null,
        exception: e is Exception ? e : Exception(e.toString()),
      );
    }
  }

  /// private utility methods
  Result<String> _handleOkTokenPairResult(TokenPair? tokenPair) {
    if (tokenPair == null) {
      return NotOk.notFound(message: 'No token found');
    }

    // Try to get user_id from access token first
    String? userId = JwtUtils.getUserId(tokenPair.accessToken);

    // If not found in access token, try refresh token
    if (userId == null || userId.isEmpty) {
      userId = JwtUtils.getUserId(tokenPair.refreshToken);
    }

    // If still no user_id, return NotOk
    if (userId == null || userId.isEmpty) {
      return NotOk.notFound(message: 'User ID not found in tokens');
    }

    return Ok(userId);
  }
}
