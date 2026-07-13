// lib/features/profiles/domain/usecases/get_profile_posts_usecase.dart
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/post/posts_mapper.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/vos/get_profile_posts_request_vo.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/vos/profile_posts_response_vo.dart';
import 'package:meme_inator_front/features/profiles/domain/interfaces/iprofile_repository.dart';

/// Simple use case for fetching profile posts
/// Returns ProfilePostsResponseVo containing posts and next cursor
class GetProfilePostsUsecase {
  final IProfileRepository repository;

  GetProfilePostsUsecase({required this.repository});

  Future<Result<ProfilePostsResponseVo>> execute({
    required GetProfilePostsRequestVo request,
  }) async {
    try {
      final result = await repository.getProfilePosts(
        username: request.username,
        cursor: request.cursor,
        pageSize: request.pageSize,
      );

      return result.match(
        ok: (data) {
          // Convert the raw map response to our value object
          final posts = (data['posts'] as List)
              .map((post) => PostsMapper.fromJson(post as Map<String, dynamic>))
              .toList();
          final nextCursor = data['next_cursor'] as String?;
          
          return Ok(ProfilePostsResponseVo(
            posts: posts,
            nextCursor: nextCursor,
          ));
        },
        notOk: (notOk) => NotOk(
          statusCode: notOk.statusCode,
          message: notOk.message,
          staticMessage: notOk.staticMessage,
        ),
        error: (error) => Error(
          statusCode: error.statusCode,
          message: error.message,
          staticMessage: error.staticMessage,
          exception: error.exception,
        ),
      );
    } catch (e) {
      return Error.fromException(
        e is Exception ? e : Exception(e.toString()),
        message: 'Failed to get profile posts',
      );
    }
  }
}