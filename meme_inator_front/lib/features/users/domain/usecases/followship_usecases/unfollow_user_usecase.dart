// lib/features/users/domain/usecases/unfollow_user_usecase.dart
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/users/domain/interfaces/iuser_repository.dart';

class UnfollowUserUsecase {
  final IUserRepository repository;

  UnfollowUserUsecase(this.repository);

  Future<Result<void>> execute(String userId) {
    return repository.unfollowUser(userId);
  }
}