// apps/posts/domain/irepositories/ipost_repository.dart
import 'package:meme_inator_front/core/results.dart';
import 'package:uuid/uuid.dart';
import '../entities/post_entity.dart';

abstract class IPostRepository {
  PostEntity? getPostByPublicId(UuidValue postId);

  Result<PostEntity> savePost(PostEntity post);

  void incrementVoteCount(UuidValue postId, {int delta = 1});

  void decrementVoteCount(UuidValue postId, {int delta = 1});
}
