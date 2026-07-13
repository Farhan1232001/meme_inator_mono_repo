import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/registration/domain/entities/confirm_deregister_params_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/deregister_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/repositories/iregistration_repo.dart';

class ConfirmDeregistrationUsecase implements IUseCase<ConfirmDeregisterParamsVo, DeregisterResultVo> {
  final IRegistrationRepository _repository;

  ConfirmDeregistrationUsecase(this._repository);

  @override
  Future<Result<DeregisterResultVo>> execute({required ConfirmDeregisterParamsVo valObj}) {
    return _repository.confirmDeregistration(
      token: valObj.token,
      challengeCode: valObj.challengeCode,
    );
  }
}
