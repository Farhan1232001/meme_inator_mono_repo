import 'package:equatable/equatable.dart';

class LoginParamsVo extends Equatable {
  final String usernameOrEmail;
  final String password;
  final bool rememberMe;  

  const LoginParamsVo({
    required this.usernameOrEmail,
    required this.password,
    required this.rememberMe,
  });

  // Optional: Add validation
  bool get isValid => 
      usernameOrEmail.isNotEmpty && 
      password.isNotEmpty &&
      password.length >= 6; // Example validation

  @override
  List<Object?> get props => [usernameOrEmail, password, rememberMe];
}
