// lib/features/feeds/ui/cubit/feed_states.dart
import 'package:equatable/equatable.dart';
import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';

sealed class FeedState extends Equatable {
  const FeedState();
  
  @override
  List<Object?> get props => [];
}

class FeedInitialState extends FeedState {
  const FeedInitialState();
}

/// Feed configuration is loaded and ready
/// Contains attributes that change and vary for various feed types
class FeedLoadedState extends FeedState {
  final FeedConfig config;
  final FeedType type;
  IUseCase<dynamic, dynamic> get_feed_page_usecase;
  
  FeedLoadedState({
    required this.config,
    required this.type,
    required this.get_feed_page_usecase,
  });
  
  @override
  List<Object?> get props => [config, type, get_feed_page_usecase];
}

class FeedSwitching extends FeedState {
  const FeedSwitching();
  
  @override
  List<Object?> get props => [];
}

/// A global error that should show a snackbar/dialog
/// (NOT the pagination error - that's handled by PagingController)
/// This state happens if there is a error in backend
class FeedGlobalError extends FeedState {

  final String message;
  final String? staticMessage;
  final int statusCode; 
  final Exception? exception;

  const FeedGlobalError({
    required int statusCode, 
    required String? staticMessage, 
    required String message,  
    Exception? exception}) : statusCode=statusCode, staticMessage=staticMessage, message=message, exception=exception;
}

/// A success message (e.g., "Feed refreshed")
class FeedGlobalMessage extends FeedState {
  final String message;
  
  const FeedGlobalMessage(this.message);
  
  @override
  List<Object?> get props => [message];
}
