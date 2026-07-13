import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';
import 'package:uuid/uuid.dart';

class UpdateProfileCountersInput {
  final Uuid userId;
  final Map<String, int> increments;

  const UpdateProfileCountersInput({
    required this.userId,
    required this.increments,
  });
}

class UpdateProfileCountersUsecase
    extends IUseCase<UpdateProfileCountersInput, ProfileEntity> {
  final IProfileRepository profileRepo;

  UpdateProfileCountersUsecase(this.profileRepo);

  @override
  Future<Result<ProfileEntity>> execute({
    required UpdateProfileCountersInput valObj,
  }) async {
    throw UnimplementedError('UpdateProfileCountersUsecase.execute not implemented');
  }
}
