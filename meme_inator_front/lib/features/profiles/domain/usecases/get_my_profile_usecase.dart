import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';

/// Simple use case to fetch the current user's own profile
class GetMyProfileUsecase {
  final IProfileRepository repository;

  GetMyProfileUsecase({required this.repository});

  /// Execute the use case
  Future<Result<ProfileEntity>> execute() async {
    try {
      return await repository.getMyProfile();
    } catch (e) {
      return Error.fromException(
        e as Exception,
        message: 'Failed to get my profile: ${e.toString()}',
      );
    }
  }
}