import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';

class GetStoredTokenPairUsecase {
  final IAuthRepository _repository;

  GetStoredTokenPairUsecase(this._repository);

  Future<Result<TokenPair?>> execute() {
    return _repository.getStoredTokenPair();
  }
}