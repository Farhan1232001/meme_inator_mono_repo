import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/notifications/domain/entities/notification_entity.dart';

abstract class INotificationsRepository {
  Future<Result<List<NotificationEntity>>> getNotifications();
}