import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';
import 'package:uuid/uuid.dart';

class PatchMyProfileInput {
  final Uuid userId;
  final Map<String, dynamic> partialData;

  const PatchMyProfileInput({
    required this.userId,
    required this.partialData,
  });
}

class PatchMyProfileUsecase
    extends IUseCase<PatchMyProfileInput, ProfileEntity> {
  final IProfileRepository profileRepo;

  PatchMyProfileUsecase(this.profileRepo);

  @override
  Future<Result<ProfileEntity>> execute({
    required PatchMyProfileInput valObj,
  }) async {
    throw UnimplementedError('PatchMyProfileUsecase.execute not implemented');
  }
}
