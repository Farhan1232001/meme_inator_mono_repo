import 'package:meme_inator_front/features/feeds/domain/enums/grid_feed_type.dart';

/// Grid feed page request value object.
class GridfeedPageRequestVo {
  final GridFeedType gridFeedType;
  final String? cursor;
  final int pageSize;

  // For profile feeds
  final String? requestingUserId;
  final String? authorUsername;

  GridfeedPageRequestVo({
    required this.gridFeedType,
    this.cursor,
    required this.pageSize,
    this.requestingUserId,
    this.authorUsername,
  });
}
