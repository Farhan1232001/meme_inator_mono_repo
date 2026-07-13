import 'package:dio/dio.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/registration/data/dtos/deregister_confirm_request_dto.dart';
import 'package:meme_inator_front/features/registration/data/dtos/deregister_request_dto.dart';
import 'package:meme_inator_front/features/registration/data/dtos/registration_request_dto.dart';
import 'package:meme_inator_front/features/registration/data/dtos/registration_verify_request_dto.dart';
import 'package:meme_inator_front/features/registration/data/models/services/registration_api_service.dart';
import 'package:meme_inator_front/features/registration/domain/entities/deregister_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/registration_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/verification_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/repositories/iregistration_repo.dart';

class RegistrationRepositoryImpl implements IRegistrationRepository {
  final RegistrationApiService _apiService;

  RegistrationRepositoryImpl(this._apiService);

  @override
  Future<Result<RegistrationResultVo>> register({
    required String email,
    required String username,
    required String rawPassword,
  }) async {
    try {
      final request = RegistrationRequestDto(
        email: email,
        username: username,
        rawPassword: rawPassword,
      );
      await _apiService.register(request);
      return const Ok(RegistrationResultVo(requiresVerification: true));
    } catch (e) {
      return _handleException<RegistrationResultVo>(
        e, 
        defaultMessage: 'Registration failed',
        statusCodeMappings: {
          400: 'REGISTRATION_VALIDATION_ERROR',
        },
      );
    }
  }

  @override
  Future<Result<VerificationResultVo>> verifyRegistration({required String token}) async {
    try {
      final request = RegistrationVerifyRequestDto(token: token);
      final response = await _apiService.verifyRegistration(request);
      final result = VerificationResultVo(
        verified: response.verified,
        userId: response.userId,
        message: response.message,
      );
      return Ok(result);
    } catch (e) {
      return _handleException<VerificationResultVo>(
        e,
        defaultMessage: 'Verification failed',
        statusCodeMappings: {
          400: 'VERIFICATION_BAD_REQUEST',
          401: 'VERIFICATION_UNAUTHORIZED',
          410: 'VERIFICATION_TOKEN_EXPIRED',
        },
      );
    }
  }

  @override
  Future<Result<void>> deregister({
    required String refreshToken,
    required String rawPassword,
  }) async {
    try {
      final request = DeregisterRequestDto(
        refreshToken: refreshToken,
        rawPassword: rawPassword,
      );
      await _apiService.deregister(request);
      return const Ok(null);
    } catch (e) {
      return _handleException<void>(
        e,
        defaultMessage: 'Deregistration failed',
        statusCodeMappings: {
          400: 'DEREGISTER_BAD_REQUEST',
          401: 'DEREGISTER_UNAUTHORIZED',
          404: 'DEREGISTER_USER_NOT_FOUND',
        },
      );
    }
  }

  @override
  Future<Result<DeregisterResultVo>> confirmDeregistration({
    required String token,
    String? challengeCode,
  }) async {
    try {
      final request = DeregisterConfirmRequestDto(
        token: token,
        challengeCode: challengeCode,
      );
      final response = await _apiService.confirmDeregistration(request);
      final result = DeregisterResultVo(
        success: response.success,
        message: response.message,
      );
      return Ok(result);
    } catch (e) {
      return _handleException<DeregisterResultVo>(
        e,
        defaultMessage: 'Confirmation failed',
        statusCodeMappings: {
          400: 'CONFIRM_DEREGISTER_BAD_REQUEST',
          401: 'CONFIRM_DEREGISTER_UNAUTHORIZED',
          404: 'CONFIRM_DEREGISTER_NOT_FOUND',
          410: 'CONFIRM_DEREGISTER_EXPIRED',
        },
      );
    }
  }

  Result<T> _handleException<T>(
    dynamic error, {
    required String defaultMessage,
    required Map<int, String> statusCodeMappings,
  }) {
    if (error is DioException) {
      final statusCode = error.response?.statusCode;
      final staticMessage = statusCodeMappings[statusCode];
      
      if (staticMessage != null) {
        return NotOk<T>(
          message: error.response?.data['message'] as String,
          staticMessage: staticMessage,
          statusCode: statusCode ?? -1,
        );
      }
      
      return Error.fromException(error, message: defaultMessage);
    }
    
    return Error.fromException(error as Exception, message: 'Unexpected error');
  }

  String _getDefaultMessageForStatusCode(int? statusCode) {
    switch (statusCode) {
      case 400:
        return 'Bad request';
      case 401:
        return 'Unauthorized';
      case 404:
        return 'Not found';
      case 410:
        return 'Resource expired';
      default:
        return 'Request failed';
    }
  }
}