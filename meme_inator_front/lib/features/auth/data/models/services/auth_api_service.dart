import 'package:dio/dio.dart';
import 'package:meme_inator_front/core/api/endpoints/auth_endpoints.dart';
import 'package:meme_inator_front/features/auth/data/dtos/login_request_dto.dart';
import 'package:meme_inator_front/features/auth/data/dtos/login_response_dto.dart';
import 'package:meme_inator_front/features/auth/data/dtos/logout_request_dto.dart';
import 'package:meme_inator_front/features/auth/data/dtos/logout_response_dto.dart';
import 'package:meme_inator_front/features/auth/data/dtos/refresh_request_dto.dart';
import 'package:meme_inator_front/features/auth/data/dtos/refresh_response_dto.dart';
import 'package:retrofit/error_logger.dart';
import 'package:retrofit/http.dart';

part 'auth_api_service.g.dart';

@RestApi()
abstract class AuthApiService {
   factory AuthApiService(Dio dio, {String baseUrl}) = _AuthApiService;

  @POST(AuthEndpoints.login)
  Future<LoginResponseDto> login(
    @Body() LoginRequestDto request
  );
  @POST(AuthEndpoints.logout)
  Future<LogoutResponseDto> logout(
    @Body() LogoutRequestDto request
  );

  @POST(AuthEndpoints.refreshTokens)
  Future<RefreshResponseDto> refresh(
    @Body() RefreshRequestDto request
  );
}
