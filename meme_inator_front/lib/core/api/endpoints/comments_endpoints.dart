/// Comments Endpoints
class CommentsEndpoints {
  // Post comments
  static const String getPostComments = '/posts/{post_id}/comments';
  static const String createComment = '/posts/{post_id}/comments';
  
  // Comment management
  static const String updateComment = '/comments/{comment_id}';
  static const String deleteComment = '/comments/{comment_id}';
  
  // Nested threads
  static const String getNestedThreads = '/posts/{post_id}/nested_threads';
  static const String getPaginatedNestedThreads = '/posts/{post_id}/nested_threads/paginated';
  
  // Path parameter helpers
  static String postComments(String postId) => '/posts/$postId/comments';
  static String commentDetail(String commentId) => '/comments/$commentId';
  static String nestedThreads(String postId) => '/posts/$postId/nested_threads';
  static String paginatedNestedThreads(String postId) => '/posts/$postId/nested_threads/paginated';
}