// lib/features/home/ui/cubit/home_states.dart
// ignore_for_file: sort_constructors_first

import 'package:equatable/equatable.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';

/// States for Home Cubit
sealed class HomeState extends Equatable {
  const HomeState();
}

class HomeLoading extends HomeState {
  final FeedConfig _targetFeedConfig;
  FeedConfig get targetFeedConfig => _targetFeedConfig;

  const HomeLoading({required FeedConfig targetFeedConfig}) : _targetFeedConfig=targetFeedConfig;

  @override
  List<Object?> get props => [targetFeedConfig];
}


class HomeLoaded extends HomeState {
  final FeedConfig _currentFeedConfig;
  final bool _isMenuOpen; 
  FeedConfig get currentFeedConfig => _currentFeedConfig;
  bool get isMenuOpen => _isMenuOpen; 

  const HomeLoaded({
    required FeedConfig currentFeedConfig,
    bool isMenuOpen = false,
  }): _currentFeedConfig=currentFeedConfig, _isMenuOpen=isMenuOpen;

  HomeLoaded copyWith({
    FeedConfig? currentFeedConfig,
    bool? isMenuOpen,
  }) {
    return HomeLoaded(
      currentFeedConfig:
          currentFeedConfig ?? this.currentFeedConfig,
      isMenuOpen: isMenuOpen ?? this.isMenuOpen,
    );
  }

  @override
  List<Object?> get props => [currentFeedConfig, isMenuOpen];
}


class HomeError extends HomeState {
  HomeError({required this.errorMsg});

  final String errorMsg;
  
  @override
  List<Object?> get props => [errorMsg];
}
