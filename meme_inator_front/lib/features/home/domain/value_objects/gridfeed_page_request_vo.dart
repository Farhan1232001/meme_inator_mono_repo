import 'package:meme_inator_front/features/feeds/domain/enums/grid_feed_type.dart';

/// Grid feed page request value object.
class GridfeedPageRequestVo {
final GridFeedType feedType;
final String? cursor;
final int pageSize;
final String? requestingUserId;

GridfeedPageRequestVo({
required this.feedType,
this.cursor,
required this.pageSize,
this.requestingUserId,
});
}
