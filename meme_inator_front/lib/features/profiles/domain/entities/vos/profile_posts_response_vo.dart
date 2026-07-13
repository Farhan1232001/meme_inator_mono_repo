// lib/features/profiles/domain/entities/value_objects/profile_posts_response_vo.dart
import 'package:equatable/equatable.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

class ProfilePostsResponseVo extends Equatable {
  final List<PostEntity> posts;
  final String? nextCursor;

  const ProfilePostsResponseVo({
    required this.posts,
    this.nextCursor,
  });

  @override
  List<Object?> get props => [posts, nextCursor];
}