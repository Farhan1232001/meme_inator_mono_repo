import 'package:equatable/equatable.dart';
import 'package:meme_inator_front/features/registration/domain/entities/deregister_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/registration_result_vo.dart';
import 'package:meme_inator_front/features/registration/domain/entities/verification_result_vo.dart';

abstract class RegistrationState extends Equatable {
  const RegistrationState();

  @override
  List<Object?> get props => [];
}
/// Registratin states

class RegistrationInitial extends RegistrationState {
  const RegistrationInitial();
}

class RegistrationLoading extends RegistrationState {
  const RegistrationLoading();
}

class RegistrationSuccess extends RegistrationState {
  final RegistrationResultVo result;

  const RegistrationSuccess({required this.result});

  @override
  List<Object?> get props => [result];
}

class RegistrationVerifySuccess extends RegistrationState {
  final VerificationResultVo result;

  const RegistrationVerifySuccess({required this.result});

  @override
  List<Object?> get props => [result];
}

/// Deregistratin states

class DeregisterInitiated extends RegistrationState {
  const DeregisterInitiated();
}

class DeregisterConfirmSuccess extends RegistrationState {
  final DeregisterResultVo result;

  const DeregisterConfirmSuccess({required this.result});

  @override
  List<Object?> get props => [result];
}

class RegistrationError extends RegistrationState {
  final String message;

  const RegistrationError({required this.message});

  @override
  List<Object?> get props => [message];
}
