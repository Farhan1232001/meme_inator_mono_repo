import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';

class GetPublicProfileWithFollowshipUsecase {
  final IProfileRepository repository;

  GetPublicProfileWithFollowshipUsecase({required this.repository});

  Future<Result<ProfileEntity>> execute({
    required String profileOwnerUserId,
    String? viewerUserId,
    List<String>? fields,
  }) async {
    try {
      return await repository.getPublicProfileWithFollowshipContext(
        profileOwnerUserId: profileOwnerUserId,
        viewerUserId: viewerUserId,
        fields: fields,
      );
    } catch (e) {
      return Error.fromException(
        e is Exception ? e : Exception(e.toString()),
        message: 'Failed to get profile with followship context',
      );
    }
  }
}
