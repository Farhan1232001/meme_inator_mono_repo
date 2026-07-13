// lib/features/profiles/ui/viewmodels/followship_viewmodel.dart

// ignore_for_file: cascade_invocations

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/profiles/ui/bloc/followship_states.dart';
import 'package:meme_inator_front/features/users/domain/usecases/followship_usecases/follow_user_usecase.dart';
import 'package:meme_inator_front/features/users/domain/usecases/followship_usecases/unfollow_user_usecase.dart';

class FollowshipViewModel extends Cubit<FollowshipState> {
  final FollowUserUsecase _followUser;
  final UnfollowUserUsecase _unfollowUser;
  final String _currentUserId;

  FollowshipViewModel({
    required FollowUserUsecase followUser,
    required UnfollowUserUsecase unfollowUser,
    required String currentUserId,
  }) : _followUser = followUser,
       _unfollowUser = unfollowUser,
       _currentUserId = currentUserId,
       super(FollowshipInitial());

  Future<FollowshipResult> toggleFollow(
    String targetUserId,
    bool currentlyFollowing,
  ) async {
    if (targetUserId == _currentUserId) return FollowshipResult.error;

    emit(FollowshipLoading(targetUserId));

    final result = currentlyFollowing
        ? await _unfollowUser.execute(targetUserId)
        : await _followUser.execute(targetUserId);

    return result.match(
      ok: (_) {
        emit(FollowshipSuccess(targetUserId, !currentlyFollowing));
        return FollowshipResult.success;
      },
      notOk: (notOk) {
        final staticMsg = notOk.staticMessage;
        if (staticMsg == 'ALREADY_FOLLOWING' || staticMsg == 'NOT_FOLLOWING') {
          emit(FollowshipNotOkayed(targetUserId, notOk.message, staticMsg!));
          return FollowshipResult.notOkayed;
        } else {
          emit(FollowshipError(targetUserId, notOk.message));
          return FollowshipResult.error;
        }
      },
      error: (error) {
        emit(FollowshipError(targetUserId, error.message));
        return FollowshipResult.error;
      },
    );
  }

  bool isOwnProfile(String userId) => userId == _currentUserId;

  /// Reset any transient state (error or not‑okayed) back to initial.
  void resetState(String userId) {
    final current = state;
    if (current is FollowshipError && current.userId == userId) {
      emit(FollowshipInitial());
    } else if (current is FollowshipNotOkayed && current.userId == userId) {
      emit(FollowshipInitial());
    }
  }
}

class FollowshipResult {
  final bool isSuccess;
  final bool isError;
  final bool isNotOkayed;
  const FollowshipResult._({
    required this.isSuccess,
    required this.isError,
    required this.isNotOkayed,
  });
  static const success = FollowshipResult._(
    isSuccess: true,
    isError: false,
    isNotOkayed: false,
  );
  static const error = FollowshipResult._(
    isSuccess: false,
    isError: true,
    isNotOkayed: false,
  );
  static const notOkayed = FollowshipResult._(
    isSuccess: false,
    isError: false,
    isNotOkayed: true,
  );
}
