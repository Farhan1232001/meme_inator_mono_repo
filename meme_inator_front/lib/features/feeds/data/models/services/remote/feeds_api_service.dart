// lib/features/feeds/data/models/services/remote/feeds_api_service.dart
import 'package:dio/dio.dart';
import 'package:meme_inator_front/core/api/endpoints/feed_endpoints.dart';
import 'package:meme_inator_front/features/feeds/data/dtos/gridfeed_page_response_dto.dart';
import 'package:meme_inator_front/features/feeds/data/dtos/sectionalfeed_page_response_dto.dart';
import 'package:retrofit/retrofit.dart';

part 'feeds_api_service.g.dart';

@RestApi()
abstract class FeedsApiService {
  factory FeedsApiService(Dio dio, {String baseUrl}) = _FeedsApiService;

  @GET(
    FeedEndpoints.gridFeed
  )
  Future<GridFeedPageResponseDto> getGridFeed({
    @Query('feed_type') required String feedType,
    @Query('cursor') String? cursor,
    @Query('page_size') int? pageSize,
    @Query('requesting_user_id') String? requestingUserId,
    @Query('author_username') String? authorUsername,
  });

  @GET(
    FeedEndpoints.sectionalFeed
  )
  Future<SectionalFeedPageResponseDto> getSectionalFeed({
    @Query('feed_type') required String feedType,
    @Query('duration_unit') required String durationUnit,
    @Query('duration_window_size') int? durationWindowSize,
    @Query('cursor') String? cursor,
    @Query('requesting_user_id') String? requestingUserId,
    @Query('author_username') String? authorUsername,  
  });
}
