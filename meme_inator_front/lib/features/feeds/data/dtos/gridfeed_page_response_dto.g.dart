// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'gridfeed_page_response_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

GridFeedPageResponseDto _$GridFeedPageResponseDtoFromJson(
  Map<String, dynamic> json,
) => GridFeedPageResponseDto(
  nextCursor: json['next_cursor'] as String?,
  results: (json['results'] as List<dynamic>)
      .map((e) => PostDto.fromJson(e as Map<String, dynamic>))
      .toList(),
);

Map<String, dynamic> _$GridFeedPageResponseDtoToJson(
  GridFeedPageResponseDto instance,
) => <String, dynamic>{
  'next_cursor': instance.nextCursor,
  'results': instance.results,
};
