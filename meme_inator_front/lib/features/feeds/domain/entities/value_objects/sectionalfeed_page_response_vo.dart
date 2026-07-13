import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/duration_window_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/feed_page_response.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

/// Sectional feed response entity
class SectionalFeedPageResponseVo extends FeedPageResponseVo {
  final List<DurationWindowVo> _durationWindows;
  final String? _nextCursor;
  final bool _hasMore;

  bool get noMore => !_hasMore;

   SectionalFeedPageResponseVo({
    required List<DurationWindowVo> durationWindows,
    String? nextCursor,
    required bool hasMore,
  }): _durationWindows=durationWindows, _nextCursor=nextCursor, _hasMore=hasMore;

  String? get nextCursor => _nextCursor;
  List<DurationWindowVo> get sections => _durationWindows;
  List<List<PostEntity>> get durationWindowsAsLists =>
      _durationWindows.map((window) => window.posts).toList();
  List<PostEntity> get posts =>
      _durationWindows.expand((window) => window.posts).toList();
  bool get hasMore => _hasMore;

  List<DurationWindowVo> get durationWindows => _durationWindows;
}