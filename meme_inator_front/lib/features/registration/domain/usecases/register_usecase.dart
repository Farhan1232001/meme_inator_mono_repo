import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/registration/domain/entities/registration_params_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/registration_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/repositories/iregistration_repo.dart';

class RegisterUsecase implements IUseCase<RegistrationParamsVo, RegistrationResultVo> {
  final IRegistrationRepository _repository;

  RegisterUsecase(this._repository);

  @override
  Future<Result<RegistrationResultVo>> execute({required RegistrationParamsVo valObj}) {
    return _repository.register(
      email: valObj.email,
      username: valObj.username,
      rawPassword: valObj.rawPassword,
    );
  }
}