import 'package:equatable/equatable.dart';

class VerificationResultVo extends Equatable {
  final bool verified;
  final String userId;
  final String message;

  const VerificationResultVo({
    required this.verified,
    required this.userId,
    required this.message,
  });

  @override
  List<Object?> get props => [verified, userId, message];
}