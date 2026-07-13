import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';

class RefreshTokenUsecase {
  final IAuthRepository _repository;

  RefreshTokenUsecase(this._repository);

  Future<Result<TokenPair>> execute({required String refreshToken}) {
    return _repository.refreshToken(refreshToken: refreshToken);
  }
}
