
import 'package:json_annotation/json_annotation.dart';
part 'logout_request_dto.g.dart';

@JsonSerializable(createToJson: true)
class LogoutRequestDto {
  @JsonKey(name: 'refresh')
  final String refresh;

  LogoutRequestDto({
    required this.refresh,
  });

  factory LogoutRequestDto.fromJson(Map<String, dynamic> json) =>
      _$LogoutRequestDtoFromJson(json);

  Map<String, dynamic> toJson() => _$LogoutRequestDtoToJson(this);
}