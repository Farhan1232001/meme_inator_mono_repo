import 'package:equatable/equatable.dart';

class DeregisterResultVo extends Equatable {
  final bool success;
  final String message;

  const DeregisterResultVo({required this.success, required this.message});

  @override
  List<Object?> get props => [success, message];
}