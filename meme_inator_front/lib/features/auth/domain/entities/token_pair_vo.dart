// lib/features/auth/domain/entities/token_pair.dart
import 'package:equatable/equatable.dart';

class TokenPair extends Equatable {
  final String accessToken;
  final String refreshToken;
  final int expiresIn;
  
  const TokenPair({
    required this.accessToken,
    required this.refreshToken,
    required this.expiresIn,
  });
  
  @override
  List<Object?> get props => [accessToken, refreshToken, expiresIn];
}
