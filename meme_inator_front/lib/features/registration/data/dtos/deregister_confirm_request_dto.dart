import 'package:json_annotation/json_annotation.dart';

part 'deregister_confirm_request_dto.g.dart';

@JsonSerializable(createToJson: true)
class DeregisterConfirmRequestDto {
  @JsonKey(name: 'token')
  final String token;

  @JsonKey(name: 'challenge_code')
  final String? challengeCode;

  DeregisterConfirmRequestDto({
    required this.token,
    this.challengeCode,
  });

  factory DeregisterConfirmRequestDto.fromJson(Map<String, dynamic> json) =>
      _$DeregisterConfirmRequestDtoFromJson(json);

  Map<String, dynamic> toJson() => _$DeregisterConfirmRequestDtoToJson(this);
}
