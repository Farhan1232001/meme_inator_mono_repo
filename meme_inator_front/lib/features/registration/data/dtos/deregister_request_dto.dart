import 'package:json_annotation/json_annotation.dart';

part 'deregister_request_dto.g.dart';

@JsonSerializable(createToJson: true)
class DeregisterRequestDto {
  @JsonKey(name: 'refresh_token')
  final String refreshToken;

  @JsonKey(name: 'raw_password')
  final String rawPassword;

  DeregisterRequestDto({
    required this.refreshToken,
    required this.rawPassword,
  });

  factory DeregisterRequestDto.fromJson(Map<String, dynamic> json) =>
      _$DeregisterRequestDtoFromJson(json);

  Map<String, dynamic> toJson() => _$DeregisterRequestDtoToJson(this);
}