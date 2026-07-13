
import 'package:equatable/equatable.dart';

abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object?> get props => [];
}

class AuthLoginRequestedEvent extends AuthEvent {
  final String username;
  final String password;
  final bool rememberMe;

  const AuthLoginRequestedEvent({required this.username, required this.password, required this.rememberMe});

  @override
  List<Object?> get props => [username, password, rememberMe];
}

class AuthLogoutRequestedEvent extends AuthEvent {}

class AuthCheckStatusRequestedEvent extends AuthEvent {
  const AuthCheckStatusRequestedEvent();
}

class AuthRefreshTokenRequestedEvent extends AuthEvent {
  const AuthRefreshTokenRequestedEvent();
}
