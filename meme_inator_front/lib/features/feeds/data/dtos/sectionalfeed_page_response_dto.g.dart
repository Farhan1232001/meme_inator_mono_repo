// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'sectionalfeed_page_response_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SectionalFeedPageResponseDto _$SectionalFeedPageResponseDtoFromJson(
  Map<String, dynamic> json,
) => SectionalFeedPageResponseDto(
  durationWindows: (json['duration_windows'] as List<dynamic>)
      .map((e) => DurationWindowDto.fromJson(e as Map<String, dynamic>))
      .toList(),
  nextCursor: json['next_cursor'] as String?,
  hasMore: json['has_more'] as bool,
);

Map<String, dynamic> _$SectionalFeedPageResponseDtoToJson(
  SectionalFeedPageResponseDto instance,
) => <String, dynamic>{
  'duration_windows': instance.durationWindows,
  'next_cursor': instance.nextCursor,
  'has_more': instance.hasMore,
};
