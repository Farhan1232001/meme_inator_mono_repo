// lib/features/feeds/ui/config/feed_config.dart
// ignore_for_file: sort_constructors_first

import 'package:flutter/widgets.dart';
import 'package:meme_inator_front/features/feeds/domain/enums/grid_feed_type.dart';
import 'package:meme_inator_front/features/feeds/domain/enums/sectional_feed_type.dart';

enum FeedType { sectionalFeed, gridFeed, listFeed }

/// Feeds configurations
/// contains following information
/// 1. Feed type
/// 2. non-nullable attributes inclusive to both Feeds
/// 3. nullable attributes found only in sectional feeds.
@immutable
class FeedConfig {
  final String title;
  final FeedType type;
  final SectionalFeedType? sectionalFeedSubType;
  final GridFeedType? gridFeedSubType;
  final int pageSize;
  final String? durationUnit;
  final int? durationWindowSize;
  final bool showRefreshButton;
  final WidgetBuilder? customAppBar;

  // Sectional Feed configs
  static int defaultDurationWindowSize = 3;

  // Profile Feeds contextual parameters
  final String? authorUsername;
  final String? requestingUserId;

  const FeedConfig({
    required this.title,
    required this.type,
    required this.sectionalFeedSubType,
    required this.gridFeedSubType,
    this.pageSize = 10,
    this.durationUnit,
    this.durationWindowSize,
    this.showRefreshButton = true,
    this.customAppBar,
    this.authorUsername,
    this.requestingUserId,
  }) : assert(
         (sectionalFeedSubType == null && gridFeedSubType != null) ||
             (gridFeedSubType == null && sectionalFeedSubType != null),
         'SectionalFeedSubType OR gridFeedSubType: MUST pick one and set other to NULL',
       );

  // Predefined configurations
  factory FeedConfig.createPopularToday() => const FeedConfig(
    title: 'Popular Today',
    type: FeedType.sectionalFeed,
    sectionalFeedSubType: SectionalFeedType.POPULAR_TODAY,
    gridFeedSubType: null,
    pageSize: 10,
    durationUnit: 'day',
    durationWindowSize: 3,
  );

  factory FeedConfig.createPopularWeekly() => const FeedConfig(
    title: 'Popular this Week',
    type: FeedType.sectionalFeed,
    sectionalFeedSubType: SectionalFeedType.POPULAR_WEEKLY,
    gridFeedSubType: null,
    pageSize: 10,
    durationUnit: 'week',
    durationWindowSize: 3,
  );

  factory FeedConfig.createPopularMonthly() => const FeedConfig(
    title: 'Popular this Month',
    type: FeedType.sectionalFeed,
    sectionalFeedSubType: SectionalFeedType.POPULAR_MONTHLY,
    gridFeedSubType: null,
    pageSize: 10,
    durationUnit: 'month',
    durationWindowSize: 3,
  );

  factory FeedConfig.createRandomizedPopular() => const FeedConfig(
    title: 'Random Popular',
    type: FeedType.gridFeed,
    sectionalFeedSubType: null,
    gridFeedSubType: GridFeedType.RANDOMIZED,
    pageSize: 10,
    durationUnit: 'day',
    durationWindowSize: 7,
  );

  factory FeedConfig.createRecent() => const FeedConfig(
    title: 'Recent Posts',
    type: FeedType.gridFeed,
    sectionalFeedSubType: null,
    gridFeedSubType: GridFeedType.RECENT,
    pageSize: 15,
  );

  factory FeedConfig.createImagesOnly() => const FeedConfig(
    title: 'Images Only',
    type: FeedType.gridFeed,
    sectionalFeedSubType: null,
    gridFeedSubType: GridFeedType.IMAGES_ONLY,
    pageSize: 12,
  );

  factory FeedConfig.createVideosOnly() => const FeedConfig(
    title: 'Videos Only',
    type: FeedType.gridFeed,
    sectionalFeedSubType: null,
    gridFeedSubType: GridFeedType.VIDEOS_ONLY,
    pageSize: 15,
    showRefreshButton: true,
  );

  factory FeedConfig.createProfileConfig({
    required String username,
    required FeedType type,
  }) => FeedConfig(
    title: "$username's Posts",
    type: type,
    sectionalFeedSubType: type == FeedType.sectionalFeed
        ? SectionalFeedType.USER_PROFILES
        : null,
    gridFeedSubType: type == FeedType.gridFeed
        ? GridFeedType.USER_PROFILES
        : null,
    pageSize: 15,
    showRefreshButton: true,
    authorUsername: username,
  );

  // Private feeds below: requres auth

  factory FeedConfig.createFollowingsLiked() => const FeedConfig(
    title: 'Liked by Followings',
    type: FeedType.gridFeed,
    sectionalFeedSubType: null,
    gridFeedSubType: GridFeedType.FOLLOWINGS_POSTS,
    pageSize: 15,
    showRefreshButton: true,
  );

  factory FeedConfig.createFriendsLiked() => const FeedConfig(
    title: 'Liked by ur Friends :)',
    type: FeedType.gridFeed,
    sectionalFeedSubType: null,
    gridFeedSubType: GridFeedType.FRIENDS_POSTS,
    pageSize: 15,
    showRefreshButton: true,
  );

  factory FeedConfig.createMyLikedMemes() => const FeedConfig(
    title: 'My Liked Memes',
    type: FeedType.gridFeed,
    sectionalFeedSubType: null,
    gridFeedSubType: GridFeedType.USER_UPVOTED_POSTS,
    pageSize: 15,
    showRefreshButton: true,
  );

  factory FeedConfig.createCommentedFeeds() => const FeedConfig(
    title: 'My Comments',
    type: FeedType.gridFeed,
    sectionalFeedSubType: null,
    gridFeedSubType: GridFeedType.COMMENTED_FEEDS,
    pageSize: 15,
    showRefreshButton: true,
  );

  static FeedConfig mapSlugToFeedConfig(String feedSlug) {
    return switch (feedSlug) {
      'popular-today' => FeedConfig.createPopularToday(),
      'popular-weekly' => FeedConfig.createPopularWeekly(),
      'popular-monthly' => FeedConfig.createPopularMonthly(),
      'popular-randomized' => FeedConfig.createRandomizedPopular(),
      'recent' => FeedConfig.createRecent(),
      'images-only' => FeedConfig.createImagesOnly(),
      'videos-only' => FeedConfig.createVideosOnly(),
      'my-liked-memes' => FeedConfig.createMyLikedMemes(),
      'commented-feeds' => FeedConfig.createCommentedFeeds(),
      _ => FeedConfig.createPopularToday(),
    };
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is FeedConfig &&
          runtimeType == other.runtimeType &&
          title == other.title &&
          type == other.type &&
          pageSize == other.pageSize &&
          durationUnit == other.durationUnit &&
          durationWindowSize == other.durationWindowSize;

  @override
  int get hashCode =>
      title.hashCode ^
      type.hashCode ^
      pageSize.hashCode ^
      durationUnit.hashCode ^
      durationWindowSize.hashCode;
}
