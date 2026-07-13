// lib/features/auth/domain/usecases/get_current_user_from_token_usecase.dart
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';
import 'package:meme_inator_front/features/users/domain/entities/user_entity.dart';

/// Takes in TokenPair to and returns decoded user id. if token pair
/// not given, it will check persistent storage for stored TokenPair.
/// Otherwise, it will return null if unable to get decode. 
class GetCurrentUserFromTokenUsecase {
  final IAuthRepository _repository;

  GetCurrentUserFromTokenUsecase(this._repository);

  Future<Result<String?>> execute(TokenPair? accessToken) async {
    return await _repository.getCurrentUserViaToken(accessToken);
  }
}