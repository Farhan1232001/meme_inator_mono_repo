import 'package:json_annotation/json_annotation.dart';

part 'deregister_confirm_response_dto.g.dart';

@JsonSerializable(createToJson: true)
class DeregisterConfirmResponseDto {
  @JsonKey(name: 'success')
  final bool success;

  @JsonKey(name: 'message')
  final String message;

  DeregisterConfirmResponseDto({
    required this.success,
    required this.message,
  });

  factory DeregisterConfirmResponseDto.fromJson(Map<String, dynamic> json) =>
      _$DeregisterConfirmResponseDtoFromJson(json);

  Map<String, dynamic> toJson() => _$DeregisterConfirmResponseDtoToJson(this);
}