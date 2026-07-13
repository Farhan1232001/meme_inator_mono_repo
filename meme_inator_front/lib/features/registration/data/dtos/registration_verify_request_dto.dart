import 'package:json_annotation/json_annotation.dart';

part 'registration_verify_request_dto.g.dart';

@JsonSerializable(createToJson: true)
class RegistrationVerifyRequestDto {
  @JsonKey(name: 'token')
  final String token;

  RegistrationVerifyRequestDto({required this.token});

  factory RegistrationVerifyRequestDto.fromJson(Map<String, dynamic> json) =>
      _$RegistrationVerifyRequestDtoFromJson(json);

  Map<String, dynamic> toJson() => _$RegistrationVerifyRequestDtoToJson(this);
}