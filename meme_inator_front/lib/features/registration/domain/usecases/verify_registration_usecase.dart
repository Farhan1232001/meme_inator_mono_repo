import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/registration/domain/entities/registration_verify_params_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/verification_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/repositories/iregistration_repo.dart';

class VerifyRegistrationUsecase implements IUseCase<RegistrationVerifyParamsVo, VerificationResultVo> {
  final IRegistrationRepository _repository;

  VerifyRegistrationUsecase(this._repository);

  @override
  Future<Result<VerificationResultVo>> execute({required RegistrationVerifyParamsVo valObj}) {
    return _repository.verifyRegistration(token: valObj.token);
  }
}