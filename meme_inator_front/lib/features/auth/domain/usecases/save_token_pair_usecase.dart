import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';

class SaveTokenPairUsecase implements IUseCase<TokenPair, void> {
  final IAuthRepository _repository;

  SaveTokenPairUsecase(this._repository);

  @override
  Future<Result<void>> execute({required TokenPair valObj}) {
    return _repository.saveTokenPair(valObj);
  }
}