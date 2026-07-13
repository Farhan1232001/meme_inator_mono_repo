import 'package:dio/dio.dart';
import 'package:meme_inator_front/core/api/endpoints/registration_endpoints.dart';
import 'package:meme_inator_front/features/registration/data/dtos/deregister_confirm_request_dto.dart';
import 'package:meme_inator_front/features/registration/data/dtos/deregister_confirm_response_dto.dart';
import 'package:meme_inator_front/features/registration/data/dtos/deregister_request_dto.dart';
import 'package:meme_inator_front/features/registration/data/dtos/registration_request_dto.dart';
import 'package:meme_inator_front/features/registration/data/dtos/registration_verify_request_dto.dart';
import 'package:meme_inator_front/features/registration/data/dtos/registration_verify_response_dto.dart';
import 'package:retrofit/error_logger.dart';
import 'package:retrofit/http.dart';

part 'registration_api_service.g.dart';

@RestApi()
abstract class RegistrationApiService {
  factory RegistrationApiService(Dio dio, {String baseUrl}) = _RegistrationApiService;

  @POST(RegistrationEndpoints.register)
  Future<void> register(
    @Body() RegistrationRequestDto request
  );

  @POST(RegistrationEndpoints.verify)
  Future<RegistrationVerifyResponseDto> verifyRegistration(
    @Body() RegistrationVerifyRequestDto request
  );

  @POST(RegistrationEndpoints.deregister)
  Future<void> deregister(
    @Body() DeregisterRequestDto request
  );

  @POST(RegistrationEndpoints.confirmDeregistration)
  Future<DeregisterConfirmResponseDto> confirmDeregistration(
    @Body() DeregisterConfirmRequestDto request
  );
}
