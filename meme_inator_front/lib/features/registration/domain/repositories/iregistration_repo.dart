import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/registration/domain/entities/registration_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/verification_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/deregister_result_vo.dart';

abstract class IRegistrationRepository {
  Future<Result<RegistrationResultVo>> register({
    required String email,
    required String username,
    required String rawPassword,
  });

  Future<Result<VerificationResultVo>> verifyRegistration({
    required String token,
  });

  Future<Result<void>> deregister({
    required String refreshToken,
    required String rawPassword,
  });

  Future<Result<DeregisterResultVo>> confirmDeregistration({
    required String token,
    String? challengeCode,
  });
}