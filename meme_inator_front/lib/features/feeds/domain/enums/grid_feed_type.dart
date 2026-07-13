// ignore_for_file: constant_identifier_names

enum GridFeedType {
  RECENT('recent'),
  RANDOMIZED('randomized'),
  VIDEOS_ONLY('videos_only'),
  IMAGES_ONLY('images_only'),
  MOST_COMMENTED('most_commented'),
  USER_PROFILES('user_profile'),
  MY_POSTS('my_posts'),
  FRIENDS_POSTS('friends_posts'),
  FOLLOWINGS_POSTS('followings_posts'),

  // New private feeds
  USER_UPVOTED_POSTS('user_upvoted_posts'),
  COMMENTED_FEEDS('commented_feeds');

  final String value;
  const GridFeedType(this.value);
  @override
  String toString() => value;
}
