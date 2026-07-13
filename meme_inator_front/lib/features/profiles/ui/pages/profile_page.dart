// lib/features/profiles/ui/pages/profile_page.dart
// ignore_for_file: cascade_invocations

import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_states.dart';
import 'package:meme_inator_front/features/auth/ui/viewmodels/auth_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_profile_posts_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_public_profile_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_public_profile_with_followship_uc.dart';
import 'package:meme_inator_front/features/profiles/ui/bloc/followship_states.dart';
import 'package:meme_inator_front/features/profiles/ui/bloc/profile_states.dart';
import 'package:meme_inator_front/features/profiles/ui/viewmodels/followship_viewmodel.dart';
import 'package:meme_inator_front/features/profiles/ui/viewmodels/profile_viewmodel.dart';
import 'package:meme_inator_front/features/profiles/ui/views/profile_view.dart';
import 'package:meme_inator_front/features/profiles/ui/widgets/platform_popup_menu_button.dart';
import 'package:meme_inator_front/features/users/domain/usecases/followship_usecases/follow_user_usecase.dart';
import 'package:meme_inator_front/features/users/domain/usecases/followship_usecases/unfollow_user_usecase.dart';

class ProfilePage extends StatelessWidget {
  final String profileOwnerUserId;
  final String? currentUserId;

  const ProfilePage({
    Key? key,
    required this.profileOwnerUserId,
    this.currentUserId,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final authViewModel = context.read<AuthViewModel>();
    final authState = context.watch<AuthViewModel>().state;
    final currentUserId = authViewModel.currentUserId;
    final isAuthenticated = currentUserId != null && authState is Authenticated;

    return MultiBlocProvider(
      providers: [
        BlocProvider<ProfileViewModel>(
          create: (context) =>
              ProfileViewModel(
                getPublicProfile: GetIt.instance.get<GetPublicProfileUsecase>(),
                getPublicProfileWithFollowship: GetIt.instance
                    .get<GetPublicProfileWithFollowshipUsecase>(),
                getProfilePosts: GetIt.instance.get<GetProfilePostsUsecase>(),
                viewerUserId: currentUserId,
              )..loadProfileWithFollowshipContext(
                profileOwnerUserId,
                FeedType.gridFeed,
              ),
        ),
        // Only provide FollowshipViewModel if user is authenticated
        if (isAuthenticated)
          BlocProvider<FollowshipViewModel>(
            create: (context) => FollowshipViewModel(
              followUser: GetIt.instance.get<FollowUserUsecase>(),
              unfollowUser: GetIt.instance.get<UnfollowUserUsecase>(),
              currentUserId: currentUserId,
            ),
          ),
      ],
      child: BlocBuilder<ProfileViewModel, ProfileState>(
        builder: (context, profileState) {
          return PlatformScaffold(
            appBar:
                _buildAppBarFromState(profileState, context, isAuthenticated)
                    as PlatformAppBar?,
            body: isAuthenticated
                ? BlocListener<FollowshipViewModel, FollowshipState>(
                    listener: _handleFollowshipState,
                    child: _buildProfileContent(context, profileState),
                  )
                : _buildProfileContent(context, profileState),
          );
        },
      ),
    );
  }

  // --------------------------------------------------------------------------
  // App bar
  // --------------------------------------------------------------------------
  Widget _buildAppBarFromState(
    ProfileState profileState,
    BuildContext context,
    bool isAuthenticated,
  ) {
    if (profileState is ProfileLoaded) {
      final profile = profileState.profile;

      // If not authenticated, show simple app bar without menu
      if (!isAuthenticated) {
        return PlatformAppBar(title: Text(profile.username));
      }

      // For authenticated users, check if it's their own profile
      final followshipVM = context.read<FollowshipViewModel>();
      final isOwnProfile = followshipVM.isOwnProfile(profile.userId);
      return _buildAppBar(context, profile, isOwnProfile);
    } else if (profileState is ProfileLoading) {
      return const PlatformAppBar(title: Text('Loading...'));
    } else if (profileState is ProfileError) {
      return const PlatformAppBar(title: Text('Error'));
    } else {
      return const PlatformAppBar(title: Text('Profile'));
    }
  }

  PlatformAppBar _buildAppBar(
    BuildContext context,
    ProfileEntity profile,
    bool isOwnProfile,
  ) {
    final followshipState = context.watch<FollowshipViewModel>().state;
    final isFollowActionInProgress = followshipState is FollowshipLoading;

    return PlatformAppBar(
      title: Text(profile.username),
      trailingActions: isOwnProfile
          ? []
          : [
              BlocBuilder<ProfileViewModel, ProfileState>(
                builder: (context, profileState) {
                  final currentIsFollowing = profileState is ProfileLoaded
                      ? profileState.profile.isFollowing
                      : profile.isFollowing;

                  return PlatformPopupMenuButton<String>(
                    key: const ValueKey('profile_menu_button'),
                    enabled: !isFollowActionInProgress,
                    onSelected: (value) async {
                      if (value == 'follow' || value == 'unfollow') {
                        await _handleFollowshipTap(
                          context,
                          profile.userId,
                          currentIsFollowing!,
                        );
                      } else if (value == 'friend_request') {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Friend request sent!')),
                        );
                      }
                    },
                    itemBuilder: (context) =>
                        _buildMenuItems(currentIsFollowing!),
                    child: const Icon(Icons.more_horiz, size: 48),
                  );
                },
              ),
            ],
    );
  }

  // --------------------------------------------------------------------------
  // Follow / unfollow logic with optimistic update + rollback (local var)
  // --------------------------------------------------------------------------
  Future<void> _handleFollowshipTap(
    BuildContext context,
    String userId,
    bool currentlyFollowing,
  ) async {
    final profileVM = context.read<ProfileViewModel>();
    final currentProfile = profileVM.currentProfile;
    if (currentProfile == null) return;

    // 1. Store original for rollback
    final originalProfile = currentProfile;

    // 2. Compute optimistic values
    final newFollowingStatus = !currentlyFollowing;
    final newFollowersCount = currentlyFollowing
        ? currentProfile.followersCount - 1
        : currentProfile.followersCount + 1;

    // 3. Optimistic update
    final optimisticProfile = currentProfile.copyWith(
      isFollowing: newFollowingStatus,
      followersCount: newFollowersCount,
    );
    profileVM.updateProfile(optimisticProfile);

    // 4. Perform actual request
    final result = await context.read<FollowshipViewModel>().toggleFollow(
      userId,
      currentlyFollowing,
    );

    // 5. If the operation failed, rollback to original
    if (result.isError || result.isNotOkayed) {
      profileVM.updateProfile(originalProfile);
    }
  }

  // --------------------------------------------------------------------------
  // Followship state listener (dialogs only, rollback already done)
  // --------------------------------------------------------------------------
  void _handleFollowshipState(BuildContext context, FollowshipState state) {
    if (state is FollowshipError) {
      _showErrorDialog(context, state.message, () {
        context.read<FollowshipViewModel>().resetState(state.userId);
      });
    } else if (state is FollowshipNotOkayed) {
      // For known "already following/not following" we just refresh the profile
      // to get the real state, because our optimistic update might have been wrong.
      final profileVM = context.read<ProfileViewModel>();
      profileVM.loadProfileWithFollowshipContext(
        profileOwnerUserId,
        FeedType.gridFeed,
      );
      _showInfoDialog(context, state.message, () {
        context.read<FollowshipViewModel>().resetState(state.userId);
      });
    }
    // FollowshipSuccess – optimistic update already correct, nothing to do.
  }

  // --------------------------------------------------------------------------
  // Profile content (same as before)
  // --------------------------------------------------------------------------
  Widget _buildProfileContent(BuildContext context, ProfileState profileState) {
    // 1. Go through non-ProfileLoaded states
    if (profileState is ProfileLoading) {
      return const Center(child: PlatformCircularProgressIndicator());
    }
    if (profileState is ProfileError) {
      return Center(
        child: _buildProfileContentOnError(context, profileState),
      );
    }
    if (profileState is! ProfileLoaded) {
      return const Center(child: PlatformCircularProgressIndicator());
    }

    // 2. ProfileLoaded
    return ProfileView(username: profileState.profile.username);
  }

  // --------------------------------------------------------------------------
  // Menu items (unchanged)
  // --------------------------------------------------------------------------
  List<PopupMenuItem<String>> _buildMenuItems(bool isFollowing) {
    return [
      PopupMenuItem<String>(
        value: isFollowing ? 'unfollow' : 'follow',
        child: Row(
          children: [
            Icon(
              isFollowing ? Icons.person_remove : Icons.person_add,
              size: 20,
            ),
            const SizedBox(width: 12),
            Text(isFollowing ? 'Unfollow :|' : 'Follow :)'),
          ],
        ),
      ),
      const PopupMenuItem<String>(
        value: 'friend_request',
        child: Row(
          children: [
            Icon(Icons.person_add_alt_1, size: 20),
            SizedBox(width: 12),
            Text('Send Friend Request :o'),
          ],
        ),
      ),
    ];
  }

  // --------------------------------------------------------------------------
  // Dialogs (unchanged)
  // --------------------------------------------------------------------------
  void _showInfoDialog(
    BuildContext context,
    String message,
    VoidCallback onClose,
  ) {
    showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: const Text('Info'),
        content: Text(message),
        actions: [
          PlatformDialogAction(
            child: const Text('OK'),
            onPressed: () {
              Navigator.of(context).pop();
              onClose();
            },
          ),
        ],
      ),
    );
  }

  void _showErrorDialog(
    BuildContext context,
    String message,
    VoidCallback onClose,
  ) {
    showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: const Text('Error'),
        content: Text(message),
        actions: [
          PlatformDialogAction(
            child: const Text('OK'),
            onPressed: () {
              Navigator.of(context).pop();
              onClose();
            },
          ),
        ],
      ),
    );
  }

  Widget _buildProfileContentOnError(
    BuildContext context,
    ProfileError profileState,
  ) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(profileState.message),
        const SizedBox(height: 16),
        PlatformElevatedButton(
          onPressed: () =>
              context.read<ProfileViewModel>().loadProfileWithFollowshipContext(
                profileOwnerUserId,
                FeedType.gridFeed,
              ),
          child: const Text('Retry'),
        ),
      ],
    );
  }
}
