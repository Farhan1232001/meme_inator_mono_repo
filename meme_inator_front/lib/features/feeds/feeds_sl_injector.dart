// lib/features/feeds/feeds_injector.dart
// ignore_for_file: cascade_invocations

import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/feeds/data/models/repositories/feed_repository_impl.dart';
import 'package:meme_inator_front/features/feeds/data/models/services/remote/feeds_api_service.dart';
import 'package:meme_inator_front/features/feeds/domain/repositories/ifeed_repository.dart';
import 'package:meme_inator_front/features/feeds/domain/usecases/get_gridfeed_page_uc.dart';
import 'package:meme_inator_front/features/feeds/domain/usecases/get_sectionalfeed_page_uc.dart';


void configureFeedsDependencies(GetIt sl) {
  // API Service
  sl.registerLazySingleton<FeedsApiService>(
    () => FeedsApiService(sl<Dio>()),
  );
  
  // Repository
  sl.registerLazySingleton<IFeedRepository>(
    () => FeedRepositoryImpl(sl<FeedsApiService>()),
  );
  
  // Use Cases
  sl.registerLazySingleton<GetGridFeedUseCase>(
    () => GetGridFeedUseCase(sl<IFeedRepository>()),
  );
  
  sl.registerLazySingleton<GetSectionalFeedUseCase>(
    () => GetSectionalFeedUseCase(sl<IFeedRepository>()),
  );
  
}
