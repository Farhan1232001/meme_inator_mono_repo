import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';
import 'package:uuid/uuid.dart';


class GetProfileImageUrlsUsecase {
  final IProfileRepository profileRepo;

  GetProfileImageUrlsUsecase(this.profileRepo);

  Future<Result<Map<String, String>>> execute({
    required UuidValue userId,
  }) async {
    throw UnimplementedError('GetProfileImageUrlsUsecase.execute not implemented');
  }
}
