// apps/posts/domain/usecases/create_post_usecase.dart
import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_data_vo.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';
import 'package:meme_inator_front/features/post/domain/repositories/ipost_repository.dart';

class CreatePostUsecase implements IUseCase<PostDataVo, PostEntity> {
  final IPostRepository postRepository;

  CreatePostUsecase(this.postRepository);

  @override
  Future<Result<PostEntity>> execute({required PostDataVo valObj}) async {
    throw UnimplementedError();
  }
}
