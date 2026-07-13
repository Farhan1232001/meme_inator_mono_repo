import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/users/domain/entities/user_entity.dart';

abstract class IUserRepository {
  Future<Result<void>> followUser(String userId);
  Future<Result<void>> unfollowUser(String userId);
  Future<Result<UserEntity>> getCurrentUser();
}