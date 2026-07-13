
import 'package:json_annotation/json_annotation.dart';
part 'refresh_request_dto.g.dart';

@JsonSerializable(createToJson: true)
class RefreshRequestDto {
  @JsonKey(name: 'refresh')
  final String refresh;

  RefreshRequestDto({
    required this.refresh,
  });

  factory RefreshRequestDto.fromJson(Map<String, dynamic> json) =>
      _$RefreshRequestDtoFromJson(json);

  Map<String, dynamic> toJson() => _$RefreshRequestDtoToJson(this);
}