import 'package:equatable/equatable.dart';

class RegistrationResultVo extends Equatable {
  final bool requiresVerification;
  final String? userId;

  const RegistrationResultVo({
    required this.requiresVerification,
    this.userId,
  });

  @override
  List<Object?> get props => [requiresVerification, userId];
}