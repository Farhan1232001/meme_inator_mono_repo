import 'package:meme_inator_front/features/post/data/dtos/post_dto.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';
import 'package:uuid/uuid_value.dart';

class PostsMapper {
  /// Convert PostDto to PostEntity
  static PostEntity dtoToEntity(PostDto dto) {
    return PostEntity(
      postId: dto.postId,
      imageUrl: dto.imageUrl,
      authorId: dto.author,
      thumbnailUrl: dto.thumbnailUrl,
      caption: dto.caption,
      createdOn: DateTime.tryParse(dto.createdOn),
      postType: dto.postType,
      fileFormat: dto.fileFormat,
      likesCount: dto.likesCount,
      dislikesCount: dto.dislikesCount,
      commentsCount: dto.commentsCount,
      sharesCount: dto.sharesCount,
      tags: dto.tags,
      isFlagged: dto.isFlagged,
      isDeleted: dto.isDeleted,
      visibility: dto.visibility,
    );
  }

  /// Convert PostEntity to PostDto
  static PostDto entityToDto(PostEntity entity) {
    return PostDto(
      postId: entity.postId,
      author: entity.authorId,
      imageUrl: entity.imageUrl,
      thumbnailUrl: entity.thumbnailUrl ?? '',
      caption: entity.caption ?? '',
      createdOn: entity.createdOn?.toIso8601String() ?? '',
      postType: entity.postType ?? '',
      fileFormat: entity.fileFormat ?? '',
      likesCount: entity.likesCount,
      dislikesCount: entity.dislikesCount,
      commentsCount: entity.commentsCount,
      sharesCount: entity.sharesCount,
      tags: entity.tags,
      isFlagged: entity.isFlagged,
      isDeleted: entity.isDeleted,
      visibility: entity.visibility ?? 'public',
    );
  }

  /// Convert PostEntity to PostDataVo (simplified version)
  static Map<String, dynamic> entityToPostDataVo(PostEntity entity) {
    return {
      'image_url': entity.imageUrl,
      'author_id': entity.authorId,
      'thumbnail_url': entity.thumbnailUrl,
      'caption': entity.caption,
      'post_type': entity.postType,
      'file_format': entity.fileFormat,
      'tags': entity.tags,
      'visibility': entity.visibility,
    };
  }

  static PostEntity fromJson(Map<String, dynamic> json) {
    return PostEntity(
      postId: UuidValue.fromString(json['postId'] as String),
      imageUrl: json['imageUrl'] as String,
      authorId: UuidValue.fromString(json['authorId'] as String),
      thumbnailUrl: json['thumbnailUrl'] as String?,
      caption: json['caption'] as String?,
      createdOn: json['createdOn'] != null 
          ? DateTime.parse(json['createdOn'] as String) 
          : null,
      postType: json['postType'] as String?,
      fileFormat: json['fileFormat'] as String?,
      likesCount: json['likesCount'] as int? ?? 0,
      dislikesCount: json['dislikesCount'] as int? ?? 0,
      commentsCount: json['commentsCount'] as int? ?? 0,
      sharesCount: json['sharesCount'] as int? ?? 0,
      tags: (json['tags'] as List<dynamic>?)
          ?.map((tag) => tag as String)
          .toList() ?? [],
      isFlagged: json['isFlagged'] as bool? ?? false,
      isDeleted: json['isDeleted'] as bool? ?? false,
      visibility: json['visibility'] as String?,
    );
  }

  static Map<String, dynamic> toJson(PostEntity entity) {
    return {
      'postId': entity.postId.toString(),
      'imageUrl': entity.imageUrl,
      'authorId': entity.authorId.toString(),
      'thumbnailUrl': entity.thumbnailUrl,
      'caption': entity.caption,
      'createdOn': entity.createdOn?.toIso8601String(),
      'postType': entity.postType,
      'fileFormat': entity.fileFormat,
      'likesCount': entity.likesCount,
      'dislikesCount': entity.dislikesCount,
      'commentsCount': entity.commentsCount,
      'sharesCount': entity.sharesCount,
      'tags': entity.tags,
      'isFlagged': entity.isFlagged,
      'isDeleted': entity.isDeleted,
      'visibility': entity.visibility,
    };
  }


}
