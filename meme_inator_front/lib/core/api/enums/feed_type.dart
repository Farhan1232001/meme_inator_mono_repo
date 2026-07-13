/// Feed type enums for grid and sectional feeds
enum GridFeedType {
  recent('recent'),
  randomized('randomized'),
  videosOnly('videos_only'),
  imagesOnly('images_only'),
  mostCommented('most_commented'),
  myPosts('my_posts'),
  friends('friends'),
  following('following');

  final String value;
  const GridFeedType(this.value);
  
  @override
  String toString() => value;
}

enum SectionalFeedType {
  popularToday('popular-today'),
  popularWeekly('popular-weekly'),
  popularMonthly('popular-monthly');

  final String value;
  const SectionalFeedType(this.value);
  
  @override
  String toString() => value;
}