// lib/features/home/ui/viewmodels/home_vm.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/feeds/ui/controllers/home_feed_controller.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/home/ui/cubit/home_states.dart';

/// Responsibilities: 
///   tracking currently selected feed configuration & isMenuOpen
///   delegates feed switching to HomeFeedController
class HomeViewModel extends Cubit<HomeState> {
  final HomeFeedController _feedController;
  
  HomeState? _previousState;
  HomeState? get previousState => _previousState;
  
  // Expose the current feed ViewModel from controller
  FeedViewModel? get currentFeedViewModel => _feedController.currentFeedViewModel;

  HomeViewModel({required HomeFeedController feedController}) 
      : _feedController = feedController,
        super(HomeLoading(targetFeedConfig: FeedConfig.createPopularToday())) {
    // Initialize with default feed
    final defaultFeedConfig = FeedConfig.createPopularToday();
    emit(HomeLoaded(currentFeedConfig: defaultFeedConfig));
  }

  void toggleMenu() {
    final currentState = state as HomeLoaded;
    emit(currentState.copyWith(isMenuOpen: !currentState.isMenuOpen));
  }

  Future<void> selectFeed(FeedConfig newFeedConfig) async {
    final currentState = state as HomeLoaded;
    if (newFeedConfig == currentState.currentFeedConfig) return;

    // Emit loading state
    emit(HomeLoading(targetFeedConfig: newFeedConfig));
    
    // Delegate to controller for actual feed switching/caching
    // logic is delegated so that the controller can orchestrate with FeedViewModel if needed
    await _feedController.switchToFeed(newFeedConfig);
    
    // Emit loaded state with new config
    emit(HomeLoaded(
      currentFeedConfig: newFeedConfig,
      isMenuOpen: false,
    ));
  }
}
