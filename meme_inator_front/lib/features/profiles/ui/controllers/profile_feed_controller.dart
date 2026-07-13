// lib/features/profiles/ui/controllers/profile_feed_controller.dart
import 'package:flutter/widgets.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/feeds/data/models/repositories/feed_repository_impl.dart';
import 'package:meme_inator_front/features/feeds/data/models/services/remote/feeds_api_service.dart';
import 'package:meme_inator_front/features/feeds/domain/repositories/ifeed_repository.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';

/// Specialized controller for profile feeds
/// Manages feed lifecycle specifically for profile posts
/// TODO: Is Controller term appropriate? Maybe Orchestrator or Operator? CacheService? 
/// Controller in flutter ecosystem implies object that manages state and interactions of a ui element.
/// Controller here implies a component that handles the logic/behavior of part of an application. 
class ProfileFeedController {
  FeedViewModel? _currentFeedViewModel;
  
  // Cache for different profile feeds (if user switches between profiles)
  final Map<String, FeedViewModel> _profileFeedCache = {};
  
  ProfileFeedController();
  
  FeedViewModel? get currentFeedViewModel => _currentFeedViewModel;
  
  /// Initialize a profile feed, but check cached feeds first
  Future<void> getOrInitProfileFeed(String username, FeedType type) async {
    // Create profile-specific feed config with username
    final profileConfig = FeedConfig.createProfileConfig(username: username, type: type);
    final cacheKey = _generateCacheKey(username);
    
    // Clean up previous ViewModel if it exists and we're not caching it
    if (_currentFeedViewModel != null && 
        !_profileFeedCache.containsKey(cacheKey)) {
      await _currentFeedViewModel?.close();
    }
    
    // Check cache or create new
    if (_profileFeedCache.containsKey(cacheKey)) {
      _currentFeedViewModel = _profileFeedCache[cacheKey];
    } else {
      final newViewModel = FeedViewModel(
        feedConfig: profileConfig,
        // feedRepository: FeedRepositoryImpl(GetIt.instance.get<FeedsApiService>()),
        feedRepository: GetIt.instance.get<IFeedRepository>(),
      );
      _profileFeedCache[cacheKey] = newViewModel;
      _currentFeedViewModel = newViewModel;
    }
    
    debugPrint('ProfileFeedController.initializeForProfile, _currentFeedViewModel=$_currentFeedViewModel');
    debugPrint('ProfileFeedController.initializeForProfile, _profileFeedCache=$_profileFeedCache');
    // Clean up old cache entries
    await _cleanupCache();
  }
  
  String _generateCacheKey(String? username) {
    return 'profile_${username ?? 'anonymous'}';
  }
  
  Future<void> _cleanupCache() async {
    const maxCacheSize = 5; // Store up to 5 different profiles
    if (_profileFeedCache.length > maxCacheSize) {
      final keysToRemove = _profileFeedCache.keys.take(
        _profileFeedCache.length - maxCacheSize
      ).toList();
      
      for (final key in keysToRemove) {
        final viewModel = _profileFeedCache[key];
        await viewModel?.close();
        _profileFeedCache.remove(key);
      }
    }
  }
  
  Future<void> dispose() async {
    for (final viewModel in _profileFeedCache.values) {
      await viewModel.close();
    }
    _profileFeedCache.clear();
    _currentFeedViewModel = null;
  }

  Future<void> refreshFeed() async {
    await _currentFeedViewModel?.refreshFeed();
  }

  void clearFeedRepository() {
    _currentFeedViewModel?.clearFeedRepository();
  }

}
