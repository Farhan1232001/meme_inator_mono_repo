import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';
import 'package:uuid/uuid.dart';

class ReplaceMyProfileInput {
  final Uuid userId;
  final Map<String, dynamic> profileData;

  const ReplaceMyProfileInput({
    required this.userId,
    required this.profileData,
  });
}

class ReplaceMyProfileUsecase
    extends IUseCase<ReplaceMyProfileInput, ProfileEntity> {
  final IProfileRepository profileRepo;

  ReplaceMyProfileUsecase(this.profileRepo);

  @override
  Future<Result<ProfileEntity>> execute({
    required ReplaceMyProfileInput valObj,
  }) async {
    throw UnimplementedError('ReplaceMyProfileUsecase.execute not implemented');
  }
}
