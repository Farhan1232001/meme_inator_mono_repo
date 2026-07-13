// lib/core/utils/jwt_decoder.dart
import 'dart:convert';
import 'package:logging/logging.dart';
/// Value encoded into JWT
/// Header
/// Payload (Claims & teh Data)
///   - iss (issuer)
///   - sub (subject/user_id)
///   - exp (expiration date)
///   ...
/// Signature (ensure integrety)
///   - hash created from header + payload content and signed using a private key. 
// lib/core/utils/jwt_utils.dart


class JwtUtils {
  static final _log = Logger('JwtUtils');

  /// Decodes a JWT token and returns the payload as a Map.
  /// Does NOT verify signature.
  static Map<String, dynamic>? decodeToken(String token) {
    try {
      final parts = token.split('.');
      if (parts.length != 3) return null;

      // Base64 decode the payload (second part)
      var payload = parts[1];
      // Add padding if needed
      payload = payload.replaceAll('-', '+').replaceAll('_', '/');
      switch (payload.length % 4) {
        case 2: payload += '==';
        case 3: payload += '=';
      }
      final decodedBytes = base64.decode(payload);
      final jsonString = utf8.decode(decodedBytes);
      return json.decode(jsonString) as Map<String, dynamic>?;
    } catch (e) {
      _log.warning('Failed to decode JWT token: $e');
      return null;
    }
  }

  static String? getUsername(String token) => decodeToken(token)?['username'] as String?;
  static String? getUserId(String token) => decodeToken(token)?['user_id'] as String?;
}