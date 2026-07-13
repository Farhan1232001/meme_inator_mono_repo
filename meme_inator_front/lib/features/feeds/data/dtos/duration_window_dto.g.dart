// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'duration_window_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

DurationWindowDto _$DurationWindowDtoFromJson(Map<String, dynamic> json) =>
    DurationWindowDto(
      label: json['label'] as String,
      startDate: DateTime.parse(json['window_start'] as String),
      endDate: DateTime.parse(json['window_end'] as String),
      posts: (json['posts'] as List<dynamic>)
          .map((e) => PostDto.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$DurationWindowDtoToJson(DurationWindowDto instance) =>
    <String, dynamic>{
      'label': instance.label,
      'window_start': instance.startDate.toIso8601String(),
      'window_end': instance.endDate.toIso8601String(),
      'posts': instance.posts,
    };
