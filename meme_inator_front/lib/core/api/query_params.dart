/// Query Parameter Constants (for reuse across endpoints)
class QueryParams {
  // Common pagination params
  static const String cursor = 'cursor';
  static const String pageSize = 'page_size';
  static const String limit = 'limit';

  // Feed params
  static const String type = 'type';
  static const String durationUnit = 'duration_unit';
  static const String durationWindowSize = 'duration_window_size';

  // Search params
  static const String query = 'q';

  // Comment params
  static const String depth = 'depth';
  static const String topLimit = 'top_limit';
  static const String topCursor = 'top_cursor';
  static const String replyLimit = 'reply_limit';
  static const String replyCursor = 'reply_cursor';

  // Friend request params
  static const String requestType = 'type'; // incoming/outgoing
}
