// lib/features/profiles/domain/usecases/get_public_profile_usecase.dart
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/vos/get_public_profile_request_vo.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';

/// Simple use case for fetching a public profile
class GetPublicProfileUsecase {
  final IProfileRepository repository;

  GetPublicProfileUsecase({required this.repository});

  Future<Result<ProfileEntity>> execute({
    required GetPublicProfileRequestVo request,
  }) async {
    try {
      return await repository.getPublicProfile(
        username: request.username,
        viewerUserId: request.viewerUserId,
      );
    } catch (e) {
      return Error.fromException(
        e is Exception ? e : Exception(e.toString()),
        message: 'Failed to get public profile',
      );
    }
  }
}