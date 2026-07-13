import 'package:json_annotation/json_annotation.dart';

part 'registration_verify_response_dto.g.dart';

@JsonSerializable(createToJson: true)
class RegistrationVerifyResponseDto {
  @JsonKey(name: 'verified')
  final bool verified;

  @JsonKey(name: 'user_id')
  final String userId;

  @JsonKey(name: 'message')
  final String message;

  RegistrationVerifyResponseDto({
    required this.verified,
    required this.userId,
    required this.message,
  });

  factory RegistrationVerifyResponseDto.fromJson(Map<String, dynamic> json) =>
      _$RegistrationVerifyResponseDtoFromJson(json);

  Map<String, dynamic> toJson() => _$RegistrationVerifyResponseDtoToJson(this);
}