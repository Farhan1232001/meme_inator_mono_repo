// ignore_for_file: constant_identifier_names

enum SectionalFeedType {
  POPULAR_TODAY('popular-today'),
  POPULAR_WEEKLY('popular-weekly'),
  POPULAR_MONTHLY('popular-monthly'),
  USER_PROFILES('user_profile'),
  MY_POSTS('my_posts');

  final String value;
  const SectionalFeedType(this.value);
  @override
  String toString() => value;
}
