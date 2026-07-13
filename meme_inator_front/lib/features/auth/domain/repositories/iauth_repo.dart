// lib/features/auth/domain/repositories/iauth_repository.dart


import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/users/domain/entities/user_entity.dart';

abstract class IAuthRepository {
  Future<Result<TokenPair>> login({
    required String usernameOrEmail,
    required String password,
    required bool rememberMe
  });
  
  Future<Result<void>> logout();
  
  Future<Result<TokenPair>> refreshToken({
    required String refreshToken,
  });
  
  Future<Result<UserEntity>> getCurrentUser();
  Future<Result<String>> getCurrentUserViaToken(TokenPair? tokenPair);
  
  Future<Result<bool>> isLoggedIn();
  
  Future<Result<void>> saveTokenPair(TokenPair tokenPair);
  
  Future<Result<TokenPair?>> getStoredTokenPair();
  
  Future<Result<void>> clearTokenPair();
}