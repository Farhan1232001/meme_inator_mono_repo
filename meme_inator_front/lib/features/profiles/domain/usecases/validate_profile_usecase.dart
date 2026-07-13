import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';

class ValidateProfileInput {
  final Map<String, dynamic> profileData;

  const ValidateProfileInput({required this.profileData});
}

class ValidateProfileUsecase
    extends IUseCase<ValidateProfileInput, void> {
  final IProfileRepository profileRepo;

  ValidateProfileUsecase(this.profileRepo);

  @override
  Future<Result<void>> execute({
    required ValidateProfileInput valObj,
  }) async {
    throw UnimplementedError('ValidateProfileUsecase.execute not implemented');
  }
}
