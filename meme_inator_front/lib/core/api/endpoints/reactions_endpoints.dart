/// Reactions Endpoints
class ReactionsEndpoints {
  static const String votePost = '/posts/{post_id}/vote';
  static const String voteComment = '/comments/{comment_id}/vote';
  
  // Path parameter helpers
  static String postVote(String postId) => '/posts/$postId/vote';
  static String commentVote(String commentId) => '/comments/$commentId/vote';
}