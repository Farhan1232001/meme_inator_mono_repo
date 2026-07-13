/// Direct Messages Endpoints
class DirectMessagesEndpoints {
  static const String getConversations = '/dm/conversations';
  static const String getMessages = '/dm/conversations/{user_id}/messages';
  static const String sendMessage = '/dm/conversations/{user_id}/messages';
  
  // Path parameter helper
  static String conversationMessages(String userId) => '/dm/conversations/$userId/messages';
}