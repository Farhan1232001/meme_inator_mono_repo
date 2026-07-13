// lib/features/feeds/ui/controllers/home_feed_controller.dart
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/feeds/domain/repositories/ifeed_repository.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';

/// This controller manages feed switching and caching
/// controller acts as delegate for HomeViewModel
/// 
/// TODO: Caching is NOT working properly. pageController seems to work but NOT scrollController, within FeedViewModel that that is cached. 
/// TODO: Is Controller term appropriate? Maybe Orchestrator or Operator? CacheService? 
/// Controller in flutter ecosystem implies object that manages state and interactions of a ui element.
/// Controller here implies a component that handles the logic/behavior of part of an application. 
class HomeFeedController {
  FeedViewModel? _currentFeedViewModel;
  
  // Cache for different feed configurations to prevent deallocation
  final Map<String, FeedViewModel> _feedCache = {};
  
  HomeFeedController() {
    // Initialize with default feed
    final defaultConfig = FeedConfig.createPopularToday();
    _handleFeedSwitch(defaultConfig);
  }
  
  FeedViewModel? get currentFeedViewModel => _currentFeedViewModel;
  
  // Public method for HomeViewModel to call
  Future<void> switchToFeed(FeedConfig newConfig) async {
    _handleFeedSwitch(newConfig);
  }
  
  Future<void> _handleFeedSwitch(FeedConfig newConfig) async {
    if (_currentFeedViewModel?.feedConfig == newConfig) await _currentFeedViewModel?.refreshFeed();

    // Generate a cache key from the config
    final cacheKey = _generateCacheKey(newConfig);
    
    // Check if we already have this feed cached
    if (_feedCache.containsKey(cacheKey)) {
      _currentFeedViewModel = _feedCache[cacheKey];
    } else {
      // Create new ViewModel for this config
      final newViewModel = FeedViewModel(
        feedConfig: newConfig,
        feedRepository: GetIt.instance.get<IFeedRepository>(),
      );
      _feedCache[cacheKey] = newViewModel;
      _currentFeedViewModel = newViewModel;
    }
    await _currentFeedViewModel?.refreshFeed();
    // Clean up old cache entries if memory is a concern
    await _cleanupCache();
  }
  
  String _generateCacheKey(FeedConfig config) {
    final buffer = StringBuffer()
      ..write(config.type.toString())
      ..write('.');
    
    switch (config.type) {
      case FeedType.sectionalFeed:
        buffer.write('${config.sectionalFeedSubType}.${config.durationUnit}.${config.durationWindowSize}.${config.authorUsername}');
        break;
      case FeedType.gridFeed:
        buffer.write('${config.gridFeedSubType}.${config.pageSize}.${config.authorUsername}');
        break;
      case FeedType.listFeed:
        buffer.write('list.${config.pageSize}.${config.authorUsername}');
        break;
    }
    
    return buffer.toString();
  }
  
  // TODO: If parrticular FeedViewModel gets too large in size, deallocate it. 
  Future<void> _cleanupCache() async {
    const maxCacheSize = 7;
    if (_feedCache.length > maxCacheSize) {
      final keysToRemove = _feedCache.keys.take(_feedCache.length - maxCacheSize).toList();
      for (final key in keysToRemove) {
        final viewModel = _feedCache[key];
        await viewModel?.close();
        _feedCache.remove(key);
      }
    }
  }
  
  Future<void> dispose() async {
    for (final viewModel in _feedCache.values) {
      await viewModel.close();
    }
    _feedCache.clear();
  }
}
