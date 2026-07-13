// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'post_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

PostDto _$PostDtoFromJson(Map<String, dynamic> json) => PostDto(
  postId: uuidFromJson(json['post_id'] as String),
  author: uuidFromJson(json['author'] as String),
  imageUrl: json['imageURL'] as String,
  thumbnailUrl: json['thumbnailURL'] as String,
  caption: json['caption'] as String,
  createdOn: json['createdOn'] as String,
  postType: json['post_type'] as String,
  fileFormat: json['fileFormat'] as String,
  likesCount: (json['upvotesCount'] as num).toInt(),
  dislikesCount: (json['downvotesCount'] as num).toInt(),
  commentsCount: (json['commentsCount'] as num).toInt(),
  sharesCount: (json['sharesCount'] as num).toInt(),
  tags: (json['tags'] as List<dynamic>).map((e) => e as String).toList(),
  isFlagged: json['isFlagged'] as bool,
  isDeleted: json['isDeleted'] as bool,
  visibility: json['visibility'] as String,
);

Map<String, dynamic> _$PostDtoToJson(PostDto instance) => <String, dynamic>{
  'post_id': uuidToJson(instance.postId),
  'author': uuidToJson(instance.author),
  'imageURL': instance.imageUrl,
  'thumbnailURL': instance.thumbnailUrl,
  'caption': instance.caption,
  'createdOn': instance.createdOn,
  'post_type': instance.postType,
  'fileFormat': instance.fileFormat,
  'upvotesCount': instance.likesCount,
  'downvotesCount': instance.dislikesCount,
  'commentsCount': instance.commentsCount,
  'sharesCount': instance.sharesCount,
  'tags': instance.tags,
  'isFlagged': instance.isFlagged,
  'isDeleted': instance.isDeleted,
  'visibility': instance.visibility,
};
