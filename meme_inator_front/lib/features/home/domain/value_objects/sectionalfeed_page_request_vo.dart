import 'package:meme_inator_front/features/feeds/domain/enums/sectional_feed_type.dart';

/// Sectional feed page request.
class SectionalFeedPageRequestVo {
final SectionalFeedType feedType;
final String durationUnit;
final int durationWindowSize;
final String? cursor;

SectionalFeedPageRequestVo({
required this.feedType,
required this.durationUnit,
this.durationWindowSize = 3,
this.cursor,
});
}
