import 'package:equatable/equatable.dart';

class DeregisterParamsVo extends Equatable {
  final String refreshToken;
  final String rawPassword;

  const DeregisterParamsVo({
    required this.refreshToken,
    required this.rawPassword,
  });

  @override
  List<Object?> get props => [refreshToken, rawPassword];
}