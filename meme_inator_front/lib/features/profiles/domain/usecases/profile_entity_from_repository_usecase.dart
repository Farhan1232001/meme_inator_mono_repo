import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';

class ProfileEntityFromRepositoryInput {
  final Map<String, dynamic> raw;

  const ProfileEntityFromRepositoryInput({required this.raw});
}

class ProfileEntityFromRepositoryUsecase
    extends IUseCase<ProfileEntityFromRepositoryInput, ProfileEntity> {
  final IProfileRepository profileRepo;

  ProfileEntityFromRepositoryUsecase(this.profileRepo);

  @override
  Future<Result<ProfileEntity>> execute({
    required ProfileEntityFromRepositoryInput valObj,
  }) async {
    throw UnimplementedError(
        'ProfileEntityFromRepositoryUsecase.execute not implemented');
  }
}
