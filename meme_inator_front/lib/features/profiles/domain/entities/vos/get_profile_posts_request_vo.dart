// lib/features/profiles/domain/entities/value_objects/get_profile_posts_request_vo.dart
import 'package:equatable/equatable.dart';

class GetProfilePostsRequestVo extends Equatable {
  final String username;
  final String? cursor;
  final int pageSize;

  const GetProfilePostsRequestVo({
    required this.username,
    this.cursor,
    this.pageSize = 10,
  });

  @override
  List<Object?> get props => [username, cursor, pageSize];
}