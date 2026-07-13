import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/registration/domain/entities/deregister_params_vo.dart';
import 'package:meme_inator_front/features/registration/domain/repositories/iregistration_repo.dart';

class DeregisterUsecase implements IUseCase<DeregisterParamsVo, void> {
  final IRegistrationRepository _repository;

  DeregisterUsecase(this._repository);

  @override
  Future<Result<void>> execute({required DeregisterParamsVo valObj}) {
    return _repository.deregister(
      refreshToken: valObj.refreshToken,
      rawPassword: valObj.rawPassword,
    );
  }
}