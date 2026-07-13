// In feed_endpoints.dart
import 'package:meme_inator_front/core/api/api_endpoints_base.dart';

class FeedEndpoints {
  static const String gridFeed = '/feeds/grid_feed';
  static const String sectionalFeed = '/feeds/sectional_feed';
  
  // Or use the buildUrl method
  static String getGridFeedUrl() {
    return ApiEndpointsBase.buildUrl(gridFeed);
  }
  
  static String getSectionalFeedUrl() {
    return ApiEndpointsBase.buildUrl(sectionalFeed);
  }
}
