// apps/posts/domain/entities/post_entity.dart
import 'package:uuid/uuid.dart';

class PostEntity {
  UuidValue postId;
  String imageUrl;
  UuidValue authorId;
  String? thumbnailUrl;
  String? caption;
  DateTime? createdOn;
  String? postType;
  String? fileFormat;

  int likesCount;
  
  int dislikesCount;
  int commentsCount;
  int sharesCount;

  List<String> tags;
  bool isFlagged;
  bool isDeleted;
  String? visibility;

  PostEntity({
    required this.postId,
    required this.imageUrl,
    required this.authorId,
    this.thumbnailUrl,
    this.caption,
    this.createdOn,
    this.postType,
    this.fileFormat,
    this.likesCount = 0,
    this.dislikesCount = 0,
    this.commentsCount = 0,
    this.sharesCount = 0,
    List<String>? tags,
    this.isFlagged = false,
    this.isDeleted = false,
    this.visibility,
  }) : tags = tags ?? [];

  void setImageUrl(String url) => imageUrl = url;
  void setThumbnailUrl(String? url) => thumbnailUrl = url;
}
