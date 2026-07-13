// apps/posts/domain/usecases/delete_post_usecase.dart
import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/post/domain/repositories/ipost_repository.dart';
import 'package:uuid/uuid.dart';

class DeletePostUsecase implements IUseCase<Uuid, bool> {
  final IPostRepository postRepository;

  DeletePostUsecase(this.postRepository);

  @override
  @override
  Future<Result<bool>> execute({required Uuid valObj}) async {
    // TODO: Implement the actual delete logic using postRepository
    throw UnimplementedError();
  }
}

