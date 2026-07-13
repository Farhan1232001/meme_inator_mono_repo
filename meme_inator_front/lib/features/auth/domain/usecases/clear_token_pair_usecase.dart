import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';

class ClearTokenPairUsecase  {
  final IAuthRepository _repository;

  ClearTokenPairUsecase(this._repository);

  Future<Result<void>> execute() {
    return _repository.clearTokenPair();
  }
}
