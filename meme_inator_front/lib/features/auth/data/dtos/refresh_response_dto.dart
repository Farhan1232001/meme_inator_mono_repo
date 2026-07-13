

import 'package:json_annotation/json_annotation.dart';
part 'refresh_response_dto.g.dart';

@JsonSerializable(createToJson: true)
class RefreshResponseDto {
  @JsonKey(name: 'access')
  final String access;
  
  @JsonKey(name: 'refresh')
  final String refresh;

  RefreshResponseDto({
    required this.access,
    required this.refresh,
  });

  factory RefreshResponseDto.fromJson(Map<String, dynamic> json) =>
      _$RefreshResponseDtoFromJson(json);

  Map<String, dynamic> toJson() => _$RefreshResponseDtoToJson(this);
}
