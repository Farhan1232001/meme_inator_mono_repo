enum NotificationType {
  like('LIKE'),
  dislike('DISLIKE'),
  comment('COMMENT'),
  reply('REPLY'),
  follow('FOLLOW'),
  mention('MENTION'),
  systemAlert('SYSTEM_ALERT'),
  share('SHARE'),
  award('AWARD'),
  postMilestone('POST_MILESTONE'),
  friendRequest('FRIEND_REQUEST'),
  friendAccepted('FRIEND_ACCEPTED');

  final String value;
  const NotificationType(this.value);

  static NotificationType fromString(String value) {
    return NotificationType.values.firstWhere(
      (e) => e.value == value,
      orElse: () => NotificationType.systemAlert,
    );
  }
}