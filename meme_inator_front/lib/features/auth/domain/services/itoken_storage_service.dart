import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';

/// Mobile can use flutter_secure_storage
/// TODO: Web will need another solution. 
/// 
abstract class ITokenStorageService {
  Future<void> saveTokenPair(TokenPair tokenPair);
  Future<TokenPair?> getTokenPair();
  Future<void> clearTokenPair();
}
