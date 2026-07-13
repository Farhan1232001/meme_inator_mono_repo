import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';

class CheckLoginStatusUsecase {
  final IAuthRepository _repository;

  CheckLoginStatusUsecase(this._repository);

  Future<Result<bool>> execute() {
    return _repository.isLoggedIn();
  }
}