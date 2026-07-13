// apps/posts/domain/usecases/vote_on_post_usecase.dart
import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_data_vo.dart';
import 'package:meme_inator_front/features/post/domain/repositories/ipost_vote_repository.dart';

class VoteOnPostUsecase implements IUseCase<PostDataVo, void> {
  final IPostVoteRepository voteRepository;

  VoteOnPostUsecase(this.voteRepository);

  @override
  Future<Result<void>> execute({required PostDataVo valObj}) async {
    throw UnimplementedError();
  }
}
