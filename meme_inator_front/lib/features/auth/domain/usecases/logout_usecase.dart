import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';

class LogoutUsecase implements IUseCase<void, void> {
  final IAuthRepository _repository;

  LogoutUsecase(this._repository);

  @override
  Future<Result<void>> execute({required void valObj}) {
    return _repository.logout();
  }
}
