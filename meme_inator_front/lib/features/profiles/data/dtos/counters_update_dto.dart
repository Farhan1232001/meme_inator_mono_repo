import 'package:json_annotation/json_annotation.dart';

part 'counters_update_dto.g.dart';

@JsonSerializable()
class CountersUpdateDto {
  final Map<String, int> increments;

  CountersUpdateDto({required this.increments});

  factory CountersUpdateDto.fromJson(Map<String, dynamic> json) =>
      _$CountersUpdateDtoFromJson(json);
  Map<String, dynamic> toJson() => _$CountersUpdateDtoToJson(this);
}