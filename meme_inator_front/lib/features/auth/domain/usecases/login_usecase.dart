import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/entities/login_params_vo.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';

class LoginUsecase implements IUseCase<LoginParamsVo, TokenPair> {
  final IAuthRepository _repository;

  LoginUsecase(this._repository);

  @override
  Future<Result<TokenPair>> execute({required LoginParamsVo valObj}) {
    return _repository.login(
      usernameOrEmail: valObj.usernameOrEmail,
      password: valObj.password,
      rememberMe: valObj.rememberMe
    );
  }
}
