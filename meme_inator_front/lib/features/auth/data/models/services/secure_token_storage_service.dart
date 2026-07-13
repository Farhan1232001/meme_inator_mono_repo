import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';
import 'package:meme_inator_front/features/auth/domain/services/itoken_storage_service.dart';

/// Only stores tokens for mobile devices with in-memory caching
class SecureTokenStorage implements ITokenStorageService {
  final FlutterSecureStorage _storage;
  static const String _accessKey = 'access_token';
  static const String _refreshKey = 'refresh_token';
  static const String _expiresKey = 'expires_in';
  static const String _timestampKey = 'token_timestamp';

  // In-memory cache
  TokenPair? _cachedTokenPair;
  bool _isCacheValid = false;

  SecureTokenStorage(this._storage);

  @override
  Future<void> saveTokenPair(TokenPair tokenPair) async {
    // Update persistent storage
    await _storage.write(key: _accessKey, value: tokenPair.accessToken);
    await _storage.write(key: _refreshKey, value: tokenPair.refreshToken);
    await _storage.write(key: _expiresKey, value: tokenPair.expiresIn.toString());
    
    // Update cache
    _cachedTokenPair = tokenPair;
    _isCacheValid = true;
  }

  @override
  Future<TokenPair?> getTokenPair() async {
    // Return cached value if valid
    if (_isCacheValid) {
      return _cachedTokenPair;
    }
    
    // Otherwise load from persistent storage
    final access = await _storage.read(key: _accessKey);
    final refresh = await _storage.read(key: _refreshKey);
    final expires = await _storage.read(key: _expiresKey);
    final timestamp = await _storage.read(key: _timestampKey);
    
    if (access != null && refresh != null && expires != null && timestamp != null) {

      // Check if token is expired
      final savedTime = int.parse(timestamp);
      final expiresIn = int.parse(expires);
      final isExpired = DateTime.now().millisecondsSinceEpoch > 
                        savedTime + (expiresIn * 1000);
      
      if (isExpired) {
        // Token expired, don't return it (will trigger refresh)
        return null;
      }

      _cachedTokenPair = TokenPair(
        accessToken: access,
        refreshToken: refresh,
        expiresIn: int.parse(expires),
      );
      _isCacheValid = true;
      return _cachedTokenPair;
    }
    
    return null;
  }

  @override
  Future<void> clearTokenPair() async {
    // Clear persistent storage
    await _storage.delete(key: _accessKey);
    await _storage.delete(key: _refreshKey);
    await _storage.delete(key: _expiresKey);
    
    // Clear cache
    _cachedTokenPair = null;
    _isCacheValid = false;
  }
  
  // Optional: Method to manually invalidate cache (useful for testing or force refresh)
  void invalidateCache() {
    _isCacheValid = false;
    _cachedTokenPair = null;
  }
}
