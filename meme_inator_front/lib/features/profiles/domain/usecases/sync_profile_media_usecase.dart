import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';
import 'package:uuid/uuid.dart';

class SyncProfileMediaInput {
  final Uuid userId;
  final Map<String, dynamic> mediaPayload;

  const SyncProfileMediaInput({
    required this.userId,
    required this.mediaPayload,
  });
}

class SyncProfileMediaUsecase
    extends IUseCase<SyncProfileMediaInput, ProfileEntity> {
  final IProfileRepository profileRepo;

  SyncProfileMediaUsecase(this.profileRepo);

  @override
  Future<Result<ProfileEntity>> execute({
    required SyncProfileMediaInput valObj,
  }) async {
    throw UnimplementedError('SyncProfileMediaUsecase.execute not implemented');
  }
}
