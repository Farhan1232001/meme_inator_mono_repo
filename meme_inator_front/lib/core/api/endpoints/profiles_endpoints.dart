/// Profiles Endpoints (Public View)
class ProfilesEndpoints {
  static const String getProfile = '/profiles/{username}';
  static const String getProfilePosts = '/profiles/{username}/posts';
  
  // Path parameter helpers
  static String profileDetail(String username) => '/profiles/$username';
  static String profilePosts(String username) => '/profiles/$username/posts';
}
