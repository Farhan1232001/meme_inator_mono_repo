import 'package:equatable/equatable.dart';

class RegistrationParamsVo extends Equatable {
  final String email;
  final String username;
  final String rawPassword;

  const RegistrationParamsVo({
    required this.email,
    required this.username,
    required this.rawPassword,
  });

  bool get isValid =>
      email.isNotEmpty && username.isNotEmpty && rawPassword.isNotEmpty;

  @override
  List<Object?> get props => [email, username, rawPassword];
}