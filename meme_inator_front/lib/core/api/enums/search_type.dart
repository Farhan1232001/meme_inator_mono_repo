/// Search type enum
enum SearchType {
  posts('posts'),
  users('users'),
  tags('tags');

  final String value;
  const SearchType(this.value);
  
  @override
  String toString() => value;
}