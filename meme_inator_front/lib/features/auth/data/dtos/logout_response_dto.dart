
import 'package:json_annotation/json_annotation.dart';
part 'logout_response_dto.g.dart';

@JsonSerializable(createToJson: true)
class LogoutResponseDto {
  @JsonKey(name: 'status_code')
  final int statusCode;

  @JsonKey(name: 'static_msg')
  final String staticMsg;

  @JsonKey(name: 'message')
  final String message;

  LogoutResponseDto({
    required this.statusCode,required this.staticMsg,required this.message,
  });

  factory LogoutResponseDto.fromJson(Map<String, dynamic> json) =>
      _$LogoutResponseDtoFromJson(json);

  Map<String, dynamic> toJson() => _$LogoutResponseDtoToJson(this);
}
