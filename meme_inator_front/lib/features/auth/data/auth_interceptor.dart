// ignore_for_file: cascade_invocations

import 'package:dio/dio.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/auth/domain/services/itoken_storage_service.dart';
import 'package:logging/logging.dart';

class AuthInterceptor extends Interceptor {
  final ITokenStorageService _tokenStorageService;

  /// Needed to make NEW HTTP request to refresh access token when 401 error is caught
  final Dio _dio;
  final _log = Logger('AuthInterceptor');
  
  // To prevent multiple refresh requests
  bool _isRefreshing = false;
  final List<RequestOptions> _pendingRequests = [];

  AuthInterceptor(this._tokenStorageService, this._dio);

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    _log.fine('📤 Request to: ${options.path}');
    _log.fine('📤 Request method: ${options.method}');
    _log.fine('📤 Current headers: ${options.headers}');
    
    // Skip auth header for login and refresh endpoints
    if (!options.path.contains('/login') && !options.path.contains('/token/refresh')) {
      _log.fine('🔑 Adding auth header for non-login request');
      final tokenPair = await _tokenStorageService.getTokenPair();
      if (tokenPair != null) {
        _log.fine('✅ Token found, adding to headers');
        options.headers['Authorization'] = 'Bearer ${tokenPair.accessToken}';
        _log.fine('📤 Updated headers: ${options.headers}');
      } else {
        _log.warning('⚠️ No token available for authenticated request');
      }
    } else {
      _log.fine('🚫 Skipping auth header for login/refresh endpoint');
    }
    handler.next(options);
  }
  
  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    _log.severe('❌ Dio Error: ${err.message}');
    _log.severe('❌ Response status: ${err.response?.statusCode}');
    _log.severe('❌ Response data: ${err.response?.data}');
    _log.severe('❌ Request path: ${err.requestOptions.path}');
    _log.severe('❌ Request headers: ${err.requestOptions.headers}');
    
    // Only handle 401 errors
    if (err.response?.statusCode != 401) {
      _log.fine('➡️ Not a 401 error, passing through');
      return handler.next(err);
    }

    _log.warning('🔐 401 Unauthorized detected, attempting token refresh');

    // Skip if it's already a refresh request that failed
    if (err.requestOptions.path.contains('/token/refresh')) {
      _log.severe('❌ Refresh token request failed - forcing logout');
      // Refresh token expired - force logout
      await _tokenStorageService.clearTokenPair();
      return handler.next(err);
    }

    // Queue the request and try to refresh token
    try {
      final newTokenPair = await _refreshToken();
      if (newTokenPair != null) {
        _log.info('✅ Token refresh successful, retrying failed request');
        // Retry the failed request with new token
        final opts = err.requestOptions;
        opts.headers['Authorization'] = 'Bearer ${newTokenPair.accessToken}';
        
        final response = await _dio.fetch(opts);
        _log.fine('✅ Request retry successful');
        return handler.resolve(response);
      } else {
        _log.warning('⚠️ Token refresh returned null');
      }
    } catch (e) {
      _log.severe('❌ Token refresh failed with exception: $e');
    }

    // If refresh fails, clear tokens and pass through error
    _log.warning('⚠️ Token refresh failed, clearing tokens and passing error');
    await _tokenStorageService.clearTokenPair();
    handler.next(err);
  }

  Future<TokenPair?> _refreshToken() async {
    _log.fine('🔄 Attempting to refresh token');
    
    if (_isRefreshing) {
      _log.fine('⏳ Token refresh already in progress, waiting...');
      // Wait for the ongoing refresh to complete
      await Future.delayed(const Duration(milliseconds: 100));
      final tokenPair = await _tokenStorageService.getTokenPair();
      if (tokenPair != null) {
        _log.fine('✅ Retrieved new token from storage after waiting');
      } else {
        _log.warning('⚠️ No token available after waiting for refresh');
      }
      return tokenPair;
    }

    _isRefreshing = true;
    _log.fine('🔑 Starting token refresh process');
    
    try {
      final oldPair = await _tokenStorageService.getTokenPair();
      if (oldPair == null) {
        _log.warning('⚠️ No old token pair found for refresh');
        return null;
      }

      _log.fine('📤 Calling refresh endpoint with refresh token');
      // Call your refresh endpoint
      final response = await _dio.post(
        '/auth/token/refresh',
        data: {'refresh': oldPair.refreshToken},
      );

      _log.fine('📥 Refresh response received: ${response.statusCode}');
      
      final newPair = TokenPair(
        accessToken: response.data['access'] as String,
        refreshToken: response.data['refresh'] as String ?? oldPair.refreshToken,
        expiresIn: 3600,
      );

      await _tokenStorageService.saveTokenPair(newPair);
      _log.info('✅ New token pair saved successfully');
      return newPair;
    } on DioException catch (e) {
      _log.severe('❌ Dio error during token refresh: ${e.message}');
      _log.severe('❌ Refresh response: ${e.response?.data}');
      return null;
    } catch (e) {
      _log.severe('❌ Unexpected error during token refresh: $e');
      return null;
    } finally {
      _isRefreshing = false;
      _log.fine('🔓 Token refresh process completed');
    }
  }
}
// TODO: Delete commented code below
// AuthInterceptor that does not have dio attribute. 
// // ignore_for_file: cascade_invocations

// import 'package:dio/dio.dart';
// import 'package:meme_inator_front/features/auth/domain/services/itoken_storage_service.dart';
// import 'package:logging/logging.dart';

// class AuthInterceptor extends Interceptor {
//   final ITokenStorageService _tokenStorageService;
//   final _log = Logger('AuthInterceptor');

//   AuthInterceptor(this._tokenStorageService);

//   @override
//   Future<void> onRequest(
//     RequestOptions options,
//     RequestInterceptorHandler handler,
//   ) async {
//     _log.fine('📤 Request to: ${options.path}');
//     _log.fine('📤 Request method: ${options.method}');
//     _log.fine('📤 Current headers: ${options.headers}');
    
//     // Skip auth header for login endpoint
//     if (!options.path.contains('/login')) {
//       _log.fine('🔑 Adding auth header for non-login request');
//       final tokenPair = await _tokenStorageService.getTokenPair();
//       if (tokenPair != null) {
//         _log.fine('✅ Token found, adding to headers');
//         options.headers['Authorization'] = 'Bearer ${tokenPair.accessToken}';
//         _log.fine('📤 Updated headers: ${options.headers}');
//       } else {
//         _log.warning('⚠️ No token available for authenticated request');
//       }
//     } else {
//       _log.fine('🚫 Skipping auth header for login endpoint');
//     }
//     handler.next(options);
//   }
  
//   @override
//   void onError(DioException err, ErrorInterceptorHandler handler) {
//     _log.severe('❌ Dio Error: ${err.message}');
//     _log.severe('❌ Response status: ${err.response?.statusCode}');
//     _log.severe('❌ Response data: ${err.response?.data}');
//     _log.severe('❌ Request path: ${err.requestOptions.path}');
//     _log.severe('❌ Request headers: ${err.requestOptions.headers}');
//     handler.next(err);
//   }
// }


