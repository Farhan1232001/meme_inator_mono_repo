import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/users/domain/entities/user_entity.dart';
import 'package:meme_inator_front/features/users/domain/interfaces/iuser_repository.dart';

class GetCurrentUserUsecase {
  final IUserRepository repository;

  GetCurrentUserUsecase(this.repository);

  Future<Result<UserEntity>> execute() {
    return repository.getCurrentUser();
  }
}