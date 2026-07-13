import 'package:json_annotation/json_annotation.dart';

part 'registration_request_dto.g.dart';

@JsonSerializable(createToJson: true)
class RegistrationRequestDto {
  @JsonKey(name: 'email')
  final String email;

  @JsonKey(name: 'username')
  final String username;

  @JsonKey(name: 'raw_password')
  final String rawPassword;

  RegistrationRequestDto({
    required this.email,
    required this.username,
    required this.rawPassword,
  });

  factory RegistrationRequestDto.fromJson(Map<String, dynamic> json) =>
      _$RegistrationRequestDtoFromJson(json);

  Map<String, dynamic> toJson() => _$RegistrationRequestDtoToJson(this);
}