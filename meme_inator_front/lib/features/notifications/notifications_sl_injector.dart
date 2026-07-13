// lib/features/feeds/notifications_injector.dart
// ignore_for_file: cascade_invocations


import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/notifications/data/models/repositories/mock_notification_repo.dart';
import 'package:meme_inator_front/features/notifications/domain/repositories/notification_repository.dart';

void configureNotificationsDependencies(GetIt sl) {
  // API Service
  // sl.registerLazySingleton<NotificationsApiService>(
  //   () => NotificationsApiService(sl<Dio>()),
  // );
  
  // Repository
  sl.registerLazySingleton<INotificationsRepository>(
    MockNotificationRepository.new,
  );
  
  // Use Cases
  // sl.registerLazySingleton<GetGridFeedUseCase>(
  //   () => GetGridFeedUseCase(sl<IFeedRepository>()),
  // );

  
}
