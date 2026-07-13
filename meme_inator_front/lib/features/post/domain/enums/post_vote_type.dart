// apps/posts/domain/enums/post_vote_type_enum.dart
enum PostVoteTypeEnum {
  upvote('upvote'),
  downvote('downvote');

  final String value;
  const PostVoteTypeEnum(this.value);

  static PostVoteTypeEnum fromString(String value) {
    return PostVoteTypeEnum.values.firstWhere(
      (e) => e.value == value.toLowerCase(),
      orElse: () => throw ArgumentError('Invalid vote type: $value'),
    );
  }
}
