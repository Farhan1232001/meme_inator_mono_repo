import 'package:meme_inator_front/features/feeds/domain/enums/sectional_feed_type.dart';

/// Sectional feed page request.
class SectionalFeedPageRequestVo {
  final SectionalFeedType sectionalFeedType;
  final String durationUnit;
  final int durationWindowSize;
  final String? cursor;

  // For profile feeds
  final String? requestingUserId;
  final String? authorUsername;

  SectionalFeedPageRequestVo({
    required this.sectionalFeedType,
    required this.durationUnit,
    this.durationWindowSize = 3,
    this.cursor,
    this.authorUsername,
    this.requestingUserId,
  });
}
