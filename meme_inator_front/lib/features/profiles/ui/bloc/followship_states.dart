// lib/features/profiles/ui/bloc/followship_states.dart

import 'package:equatable/equatable.dart';

abstract class FollowshipState extends Equatable {
  const FollowshipState();
  @override
  List<Object?> get props => [];
}

class FollowshipInitial extends FollowshipState {}

class FollowshipLoading extends FollowshipState {
  final String userId;
  const FollowshipLoading(this.userId);
  @override
  List<Object?> get props => [userId];
}

class FollowshipSuccess extends FollowshipState {
  final String userId;
  final bool isFollowing;
  const FollowshipSuccess(this.userId, this.isFollowing);
  @override
  List<Object?> get props => [userId, isFollowing];
}

/// The action was not allowed because the user is already following
/// (when trying to follow) or already not following (when trying to unfollow).
class FollowshipNotOkayed extends FollowshipState {
  final String userId;
  final String message;
  final String staticMessage; // add this
  FollowshipNotOkayed(this.userId, this.message, this.staticMessage);
}

class FollowshipError extends FollowshipState {
  final String userId;
  final String message;
  const FollowshipError(this.userId, this.message);
  @override
  List<Object?> get props => [userId, message];
}