// apps/posts/domain/entities/post_data_vo.dart
import 'package:uuid/uuid.dart';

class PostDataVo {
  final String imageUrl;
  final UuidValue authorId;
  final String? thumbnailUrl;
  final String? caption;
  final String? postType;
  final String? fileFormat;
  final List<String> tags;
  final String? visibility;

  PostDataVo({
    required this.imageUrl,
    required this.authorId,
    this.thumbnailUrl,
    this.caption,
    this.postType,
    this.fileFormat,
    List<String>? tags,
    this.visibility,
  }) : tags = tags ?? [] {
    _validate();
  }

  void _validate() {
    if (imageUrl.isEmpty) {
      throw ArgumentError('Image URL is required');
    }

    if (!_isValidUrl(imageUrl)) {
      throw ArgumentError('Image URL must be a valid URL');
    }

    if (thumbnailUrl != null && !_isValidUrl(thumbnailUrl!)) {
      throw ArgumentError('Thumbnail URL must be a valid URL');
    }
  }

  bool _isValidUrl(String url) {
    return url.startsWith('http://') || url.startsWith('https://');
  }

  factory PostDataVo.fromMap(Map<String, dynamic> data) {
    return PostDataVo(
      imageUrl: (data['image_url'] ?? data['imageURL'] ?? '') as String,
      authorId: data['author_id'] as UuidValue,
      thumbnailUrl: (data['thumbnail_url'] ?? data['thumbnailURL']) as String?,
      caption: data['caption'] as String?,
      postType: data['post_type'] as String?,
      fileFormat: data['file_format'] as String?,
      tags: List<String>.from((data['tags'] as List<dynamic>?) ?? []),
      visibility: data['visibility'] as String?,
    );
  }
}
