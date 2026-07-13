/// To what a Notificaition is associated with. 
enum AssociationType {
  post('post'),
  comment('comment'),
  profile('profile'),
  tag('tag'),
  award('award');

  final String value;
  const AssociationType(this.value);

  static AssociationType fromString(String value) {
    return AssociationType.values.firstWhere(
      (e) => e.value == value,
      orElse: () => AssociationType.post,
    );
  }
}