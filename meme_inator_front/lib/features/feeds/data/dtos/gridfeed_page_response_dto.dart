import 'package:json_annotation/json_annotation.dart';
import 'package:meme_inator_front/features/post/data/dtos/post_dto.dart';

part 'gridfeed_page_response_dto.g.dart';  // Add this line

@JsonSerializable(createToJson: true)
class GridFeedPageResponseDto {
  @JsonKey(name: 'next_cursor')
  final String? nextCursor;
  
  final List<PostDto> results;

  GridFeedPageResponseDto({
    this.nextCursor,
    required this.results,
  });

  factory GridFeedPageResponseDto.fromJson(Map<String, dynamic> json) =>
      _$GridFeedPageResponseDtoFromJson(json);

  Map<String, dynamic> toJson() => _$GridFeedPageResponseDtoToJson(this);
}