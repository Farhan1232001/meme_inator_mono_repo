

import 'package:equatable/equatable.dart';
import 'package:meme_inator_front/features/auth/domain/entities/token_pair_vo.dart';

abstract class AuthState extends Equatable {
  const AuthState();

  @override
  List<Object?> get props => [];
}

class AuthInitialState extends AuthState {
  const AuthInitialState();
}

class AuthLoadingState extends AuthState {
  const AuthLoadingState();
}

class Authenticated extends AuthState {
  final TokenPair tokenPair;

  const Authenticated({required this.tokenPair});

  @override
  List<Object?> get props => [tokenPair];
}

class UnauthenticatedState extends AuthState {
  final String? clearMessage;

  const UnauthenticatedState({this.clearMessage});

  @override
  List<Object?> get props => [clearMessage];
}

class AuthErrorState extends AuthState {
  final String message;

  const AuthErrorState({required this.message});

  @override
  List<Object?> get props => [message];
}
