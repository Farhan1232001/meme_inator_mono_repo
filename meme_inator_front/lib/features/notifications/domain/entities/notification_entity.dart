import 'package:equatable/equatable.dart';
import 'package:meme_inator_front/features/notifications/domain/enums/association_type.dart';
import 'package:meme_inator_front/features/notifications/domain/enums/notification_type.dart';

class NotificationEntity extends Equatable {
  final String notificationId; // UUID as string
  final String? recipientId;
  final String? senderId;
  final String? senderAvatarUrl;
  final NotificationType notificationType;
  final String message;
  final bool isRead;
  final DateTime createdAt;
  final String? associationId;
  final AssociationType? associationType;

  const NotificationEntity({
    required this.notificationId,
    this.recipientId,
    this.senderId,
    this.senderAvatarUrl,
    required this.notificationType,
    required this.message,
    required this.isRead,
    required this.createdAt,
    this.associationId,
    this.associationType,
  });

  NotificationEntity copyWith({bool? isRead}) {
    return NotificationEntity(
      notificationId: notificationId,
      recipientId: recipientId,
      senderId: senderId,
      senderAvatarUrl: senderAvatarUrl,
      notificationType: notificationType,
      message: message,
      isRead: isRead ?? this.isRead,
      createdAt: createdAt,
      associationId: associationId,
      associationType: associationType,
    );
  }

  @override
  List<Object?> get props => [
        notificationId,
        recipientId,
        senderId,
        senderAvatarUrl,
        notificationType,
        message,
        isRead,
        createdAt,
        associationId,
        associationType,
      ];
}