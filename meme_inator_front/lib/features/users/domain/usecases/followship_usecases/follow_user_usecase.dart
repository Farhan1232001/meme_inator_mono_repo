// lib/features/users/domain/usecases/follow_user_usecase.dart
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/users/domain/interfaces/iuser_repository.dart';

class FollowUserUsecase {
  final IUserRepository repository;

  FollowUserUsecase(this.repository);

  Future<Result<void>> execute(String userId) {
    return repository.followUser(userId);
  }
}