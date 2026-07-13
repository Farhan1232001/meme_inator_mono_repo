import 'package:json_annotation/json_annotation.dart';
import 'package:meme_inator_front/features/post/data/dtos/post_dto.dart';

part 'duration_window_dto.g.dart';

@JsonSerializable(createToJson: true)
class DurationWindowDto {
  final String label;
  
  @JsonKey(name: 'window_start')
  final DateTime startDate;
  
  @JsonKey(name: 'window_end')
  final DateTime endDate;
  
  final List<PostDto> posts;

  DurationWindowDto({
    required this.label,
    required this.startDate,
    required this.endDate,
    required this.posts,
  });

  factory DurationWindowDto.fromJson(Map<String, dynamic> json) =>
      _$DurationWindowDtoFromJson(json);

  Map<String, dynamic> toJson() => _$DurationWindowDtoToJson(this);
}