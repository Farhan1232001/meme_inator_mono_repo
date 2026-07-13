import 'package:equatable/equatable.dart';

class ConfirmDeregisterParamsVo extends Equatable {
  final String token;
  final String? challengeCode;

  const ConfirmDeregisterParamsVo({
    required this.token,
    this.challengeCode,
  });

  @override
  List<Object?> get props => [token, challengeCode];
}