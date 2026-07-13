import 'package:json_annotation/json_annotation.dart';
import 'package:meme_inator_front/core/utils/uuid_utils.dart';
import 'package:uuid/uuid.dart';

part 'post_dto.g.dart';

@JsonSerializable(createToJson: true)
class PostDto {
  @JsonKey(name: 'post_id', fromJson: uuidFromJson,toJson: uuidToJson,)
  final UuidValue postId;
  @JsonKey(fromJson: uuidFromJson, toJson: uuidToJson)
  final UuidValue author;
  @JsonKey(name: 'imageURL')
  final String imageUrl;
  @JsonKey(name: 'thumbnailURL')
  final String thumbnailUrl;
  final String caption;
  @JsonKey(name: 'createdOn')
  final String createdOn;
  @JsonKey(name: 'post_type')
  final String postType;
  @JsonKey(name: 'fileFormat')
  final String fileFormat;
  @JsonKey(name: 'upvotesCount')
  final int likesCount;
  @JsonKey(name: 'downvotesCount')
  final int dislikesCount;
  @JsonKey(name: 'commentsCount')
  final int commentsCount;
  @JsonKey(name: 'sharesCount')
  final int sharesCount;
  final List<String> tags;
  @JsonKey(name: 'isFlagged')
  final bool isFlagged;
  @JsonKey(name: 'isDeleted')
  final bool isDeleted;
  final String visibility;

  PostDto({
    required this.postId,
    required this.author,
    required this.imageUrl,
    required this.thumbnailUrl,
    required this.caption,
    required this.createdOn,
    required this.postType,
    required this.fileFormat,
    required this.likesCount,
    required this.dislikesCount,
    required this.commentsCount,
    required this.sharesCount,
    required this.tags,
    required this.isFlagged,
    required this.isDeleted,
    required this.visibility,
  });

  factory PostDto.fromJson(Map<String, dynamic> json) =>
      _$PostDtoFromJson(json);

  Map<String, dynamic> toJson() => _$PostDtoToJson(this);

}