import 'package:json_annotation/json_annotation.dart';
import 'package:meme_inator_front/features/feeds/data/dtos/duration_window_dto.dart';

part 'sectionalfeed_page_response_dto.g.dart'; 

@JsonSerializable(createToJson: true)
class SectionalFeedPageResponseDto {
  @JsonKey(name: 'duration_windows')
  final List<DurationWindowDto> durationWindows;
  
  @JsonKey(name: 'next_cursor')
  final String? nextCursor;
  
  @JsonKey(name: 'has_more')
  final bool hasMore;

  SectionalFeedPageResponseDto({
    required this.durationWindows,
    this.nextCursor,
    required this.hasMore,
  });

  factory SectionalFeedPageResponseDto.fromJson(Map<String, dynamic> json) =>
      _$SectionalFeedPageResponseDtoFromJson(json);

  Map<String, dynamic> toJson() => _$SectionalFeedPageResponseDtoToJson(this);
}