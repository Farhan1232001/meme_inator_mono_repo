/// Posts Endpoints
class PostsEndpoints {
  // CRUD operations
  static const String getPost = '/posts/{post_id}';
  static const String updatePost = '/posts/{post_id}';
  static const String deletePost = '/posts/{post_id}';
  
  // Path parameter helper
  static String postDetail(String postId) => '/posts/$postId';
}