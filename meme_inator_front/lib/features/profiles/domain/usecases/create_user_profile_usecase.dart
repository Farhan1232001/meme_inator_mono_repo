import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';
import 'package:uuid/uuid.dart';

class CreateUserProfileUsecase {
  final IProfileRepository profileRepo;

  CreateUserProfileUsecase(this.profileRepo);

  Future<Result<ProfileEntity>> execute({
    required UuidValue userId,
  }) async {
    throw UnimplementedError('CreateUserProfileUsecase.execute not implemented');
  }
}
