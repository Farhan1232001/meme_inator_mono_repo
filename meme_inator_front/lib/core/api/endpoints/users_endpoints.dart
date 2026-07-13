/// Users Endpoints
class UsersEndpoints {
  // Identity
  static const String getUser = '/users/{username}';
  
  // Profile Management
  static const String updateProfile = '/users/profile';
  static const String patchProfile = '/users/profile';
  
  // Settings
  static const String updateSettings = '/users/settings';
  static const String updateVisibility = '/users/settings/visibility';
  
  // Credentials
  static const String changeUsername = '/users/credentials/change-username';
  static const String changePassword = '/users/credentials/change-password';
  
  // Social Actions (Following)
  static const String followUser = '/users/{user_id}/follow';
  static const String unfollowUser = '/users/{user_id}/unfollow';
  static const String getFollowers = '/users/followers';
  static const String getFollowing = '/users/following';
  
  // Friend Requests
  static const String sendFriendRequest = '/users/{user_id}/friend_request';
  static const String getFriendRequests = '/users/friend_requests';
  static const String manageFriendRequest = '/users/friend_requests/{request_id}';
  static const String unfriend = '/users/{user_id}/friend';
  
  // Path parameter helpers
  static String userDetail(String username) => '/users/$username';
  static String follow(String userId) => '/users/$userId/follow';
  static String unfollow(String userId) => '/users/$userId/unfollow';
  static String friendRequest(String userId) => '/users/$userId/friend_request';
  static String friendRequestDetail(String requestId) => '/users/friend_requests/$requestId';
  static String removeFriend(String userId) => '/users/$userId/friend';
}