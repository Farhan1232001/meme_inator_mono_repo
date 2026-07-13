// apps/posts/domain/entities/post_vote_entity.dart
import 'package:meme_inator_front/features/post/domain/enums/post_vote_type.dart';
import 'package:uuid/uuid.dart';

class PostVoteEntity {
  final int id;
  final UuidValue publicId;
  final UuidValue postPublicId;
  final UuidValue userId;
  final PostVoteTypeEnum voteType;
  final DateTime createdAt;
  final DateTime? updatedAt;

  PostVoteEntity({
    required this.id,
    required this.publicId,
    required this.postPublicId,
    required this.userId,
    required this.voteType,
    required this.createdAt,
    this.updatedAt,
  });
}
