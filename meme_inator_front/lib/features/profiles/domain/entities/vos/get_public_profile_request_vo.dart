// lib/features/profiles/domain/entities/value_objects/get_public_profile_request_vo.dart
import 'package:equatable/equatable.dart';

class GetPublicProfileRequestVo extends Equatable {
  final String username;
  final String? viewerUserId;

  const GetPublicProfileRequestVo({
    required this.username,
    this.viewerUserId,
  });

  @override
  List<Object?> get props => [username, viewerUserId];
}