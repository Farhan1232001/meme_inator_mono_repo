import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/feed_page_response.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

/// Grid feed response entity
class GridFeedPageResponseVo extends FeedPageResponseVo {
  final String? nextCursor;
  final List<PostEntity> results;

  GridFeedPageResponseVo({
    this.nextCursor,
    required this.results,
  });

}