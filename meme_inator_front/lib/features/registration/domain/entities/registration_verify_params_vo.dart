import 'package:equatable/equatable.dart';

class RegistrationVerifyParamsVo extends Equatable {
  final String token;

  const RegistrationVerifyParamsVo({required this.token});

  @override
  List<Object?> get props => [token];
}