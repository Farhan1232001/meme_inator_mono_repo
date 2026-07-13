

import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/notifications/domain/entities/notification_entity.dart';
import 'package:meme_inator_front/features/notifications/domain/enums/notification_type.dart';
import 'package:meme_inator_front/features/notifications/domain/repositories/notification_repository.dart';

class MockNotificationRepository implements INotificationsRepository {
  @override
  Future<Result<List<NotificationEntity>>> getNotifications() async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 500));

    final now = DateTime.now();
    final notifications = [
      NotificationEntity(
        notificationId: '1',
        senderId: 'user123',
        senderAvatarUrl: null,
        notificationType: NotificationType.like,
        message: 'John Doe liked your meme',
        isRead: false,
        createdAt: now.subtract(const Duration(minutes: 5)),
      ),
      NotificationEntity(
        notificationId: '2',
        senderId: 'user456',
        senderAvatarUrl: null,
        notificationType: NotificationType.comment,
        message: 'Jane Smith commented: "This is hilarious!"',
        isRead: false,
        createdAt: now.subtract(const Duration(hours: 2)),
      ),
      NotificationEntity(
        notificationId: '3',
        senderId: 'user789',
        senderAvatarUrl: null,
        notificationType: NotificationType.friendRequest,
        message: 'Alice Johnson sent you a friend request',
        isRead: true,
        createdAt: now.subtract(const Duration(days: 1)),
      ),
      NotificationEntity(
        notificationId: '4',
        senderId: 'user101',
        senderAvatarUrl: null,
        notificationType: NotificationType.dislike,
        message: 'Bob Williams disliked your post',
        isRead: false,
        createdAt: now.subtract(const Duration(hours: 12)),
      ),
      NotificationEntity(
        notificationId: '5',
        senderId: 'user202',
        senderAvatarUrl: null,
        notificationType: NotificationType.follow,
        message: 'Emma Brown started following you',
        isRead: false,
        createdAt: now.subtract(const Duration(days: 2)),
      ),
    ];
    return Ok(notifications);
  }
}