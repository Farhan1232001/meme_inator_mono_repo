// apps/posts/domain/irepositories/ipost_vote_repository.dart
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_vote_entity.dart';
import 'package:meme_inator_front/features/post/domain/enums/post_vote_type.dart';
import 'package:uuid/uuid.dart';


abstract class IPostVoteRepository {
  Result<PostVoteEntity> voteOnPost(
    UuidValue postPublicId,
    UuidValue userId,
    PostVoteTypeEnum voteType,
  );

  Result<bool> removeVote(
    UuidValue postPublicId,
    UuidValue userId,
  );

  Result<PostVoteEntity?> getUserVote(
    UuidValue postPublicId,
    UuidValue userId,
  );

  Result<Map<String, int>> getPostVoteStats(
    UuidValue postPublicId,
  );

  bool doesPostExist(UuidValue postPublicId);
}
