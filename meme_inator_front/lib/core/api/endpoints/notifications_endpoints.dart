/// Notifications Endpoints
class NotificationsEndpoints {
  static const String getNotifications = '/notifications';
  static const String clearNotifications = '/notifications';
  static const String markAsRead = '/notifications/{id}/read';
  
  // Path parameter helper
  static String markNotificationRead(String notificationId) => '/notifications/$notificationId/read';
}