import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/feed_page_response.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_request_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_response_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_request_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_response_vo.dart';

abstract class IFeedRepository {
  /// Holds nextCursor from the last response
  FeedPageResponseVo? lastPagedResponseVo;
  
  Future<Result<GridFeedPageResponseVo>> getGridFeed(
        GridfeedPageRequestVo request
  );
  
  Future<Result<SectionalFeedPageResponseVo>> getSectionalFeed(
        SectionalFeedPageRequestVo request,
  );

  void clearLastPagedResponse() {
    lastPagedResponseVo = null;
  }
}
