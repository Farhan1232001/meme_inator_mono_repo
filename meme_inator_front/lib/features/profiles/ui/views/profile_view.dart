// lib/features/profiles/ui/views/profile_view.dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_states.dart';
import 'package:meme_inator_front/features/auth/ui/viewmodels/auth_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/views/sliver_grid_feed_view.dart';
import 'package:meme_inator_front/features/feeds/ui/views/sliver_sectional_feed_view.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/ui/bloc/followship_states.dart';
import 'package:meme_inator_front/features/profiles/ui/bloc/profile_states.dart';
import 'package:meme_inator_front/features/profiles/ui/viewmodels/followship_viewmodel.dart';
import 'package:meme_inator_front/features/profiles/ui/viewmodels/profile_viewmodel.dart';
import 'package:meme_inator_front/features/profiles/ui/widgets/seek_bar.dart';

class ProfileView extends StatelessWidget {
  final String username;

  const ProfileView({super.key, required this.username});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<ProfileViewModel, ProfileState>(
      builder: (context, state) {
        return switch (state) {
          ProfileLoaded(profile: final profile) => _buildLoaded(
            context,
            profile,
          ),
          ProfileLoading() => _buildLoading(),
          ProfileError(message: final message) => _buildError(context, message),
          _ => _buildLoading(),
        };
      },
    );
  }

  // ========== Full‑screen state builders ==========
  Widget _buildLoading() =>
      const Center(child: PlatformCircularProgressIndicator());

  Widget _buildError(BuildContext context, String message) {
    final viewModel = context.read<ProfileViewModel>();
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            '😢 Could not load profile.\n$message',
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 12),
          PlatformElevatedButton(
            onPressed: () => viewModel.loadProfile(username, FeedType.gridFeed),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.refresh),
                SizedBox(width: 8),
                Text('Retry'),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLoaded(BuildContext context, ProfileEntity profile) {
    final feedViewModel = context.read<ProfileViewModel>().feedViewModel;
    return _buildProfileContent(context, profile, feedViewModel);
  }

  // ========== Profile skeleton (feed still loading) ==========

  // ========== Full profile content with feed ==========
  Widget _buildProfileContent(
    BuildContext context,
    ProfileEntity profile,
    FeedViewModel feedViewModel,
  ) {
    final profileViewModel = context.read<ProfileViewModel>();
    return SizedBox.expand(
      child: Stack(
        children: [
          _buildBackground(context, profile),
          RefreshIndicator.adaptive(
            onRefresh: () async {
              await HapticFeedback.mediumImpact();
              // Refreshes profile contents, resets audio, and profile feed
              profileViewModel.refreshAllProfile();
            },
            child: CustomScrollView(
              slivers: [
                _buildHeaderSliver(profile),
                const SliverToBoxAdapter(child: Divider()),
                _buildProfileInfoSliver(context, profile),
                _buildBioSliver(context, profile),
                const SliverToBoxAdapter(child: Divider()),
                _buildAudioSliver(context, profile),
                const SliverToBoxAdapter(child: Divider()),
                _buildPostsHeaderSliver(),
                _buildFeedSliver(feedViewModel),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // ========== Background (box, used in Stack) ==========
  Widget _buildBackground(BuildContext context, ProfileEntity profile) {
    if (profile.bgImg?.isNotEmpty ?? false) {
      return Positioned.fill(
        child: Image.network(
          profile.bgImg!,
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => _buildFallbackBackground(),
        ),
      );
    }
    return _buildFallbackBackground();
  }

  Widget _buildFallbackBackground() => Positioned.fill(
    child: Container(color: const Color.fromARGB(255, 87, 62, 62)),
  );

  // ========== Sliver builders (return slivers directly) ==========
  Widget _buildHeaderSliver(ProfileEntity profile) {
    if (profile.profileHeaderImgUrl?.isEmpty ?? true) {
      return const SliverToBoxAdapter(child: SizedBox.shrink());
    }
    return SliverToBoxAdapter(
      child: Image.network(
        profile.profileHeaderImgUrl!,
        width: double.infinity,
        height: 200,
        fit: BoxFit.cover,
        errorBuilder: (_, __, ___) =>
            Container(height: 200, color: Colors.grey[300]),
      ),
    );
  }

  // lib/features/profiles/ui/views/profile_view.dart
  Widget _buildAudioSliver(BuildContext context, ProfileEntity profile) {
    // if (profile.profileThemeMusicUrl?.isEmpty ?? true) {
    //   return const SliverToBoxAdapter(child: SizedBox.shrink());
    // }

    final profileViewModel = context.read<ProfileViewModel>();
    final audioPlayer = profileViewModel.audioPlayer;

    return SliverToBoxAdapter(
      child: SizedBox(
        height: 50,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: AudioSlider(player: audioPlayer.rawPlayer),
        ),
      ),
    );
  }

  Widget _buildProfileInfoSliver(BuildContext context, ProfileEntity profile) {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildAvatar(profile),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        profile.username,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      _buildStatsRow(context, profile),
                    ],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAvatar(ProfileEntity profile) {
    final hasImage = (profile.profilePicUrl?.isNotEmpty ?? false);
    return Container(
      width: 100,
      height: 100,
      decoration: BoxDecoration(
        image: hasImage
            ? DecorationImage(
                image: NetworkImage(profile.profilePicUrl!),
                fit: BoxFit.cover,
              )
            : null,
        borderRadius: BorderRadius.circular(8),
        color: Colors.grey[300],
      ),
      child: hasImage
          ? null
          : const Icon(Icons.person, size: 48, color: Colors.grey),
    );
  }

  Widget _buildStatsRow(BuildContext context, ProfileEntity initialProfile) {
    final profileState = context.read<ProfileViewModel>().state;
    final profile = profileState is ProfileLoaded ? profileState.profile : null;

    final authViewModel = context.watch<AuthViewModel>();
    final authState = authViewModel.state;
    final isAuth = authState is Authenticated;

    if (!isAuth) {
      return Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatColumn('Uploads', profile?.uploadCount ?? -1),
          _buildStatColumn('Followers', profile?.followersCount ?? -1),
          _buildStatColumn('Following', profile?.followingCount ?? -1),
        ],
      );
    }

    return BlocBuilder<FollowshipViewModel, FollowshipState>(
      buildWhen: (previous, current) {
        return (previous is FollowshipLoading &&
                current is FollowshipSuccess) ||
            (previous is FollowshipLoading && current is FollowshipError) ||
            (previous is FollowshipLoading && current is FollowshipNotOkayed);
      },
      builder: (context, state) {
        // Get LATEST profile state inside the builder
        final profileState = context.watch<ProfileViewModel>().state;
        final profile = profileState is ProfileLoaded
            ? profileState.profile
            : null;
        return Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _buildStatColumn('Uploads', profile?.uploadCount ?? -1),
            _buildStatColumn('Followers', profile?.followersCount ?? -1),
            _buildStatColumn('Following', profile?.followingCount ?? -1),
          ],
        );
      },
    );
  }

  Widget _buildStatColumn(String label, int count) {
    return Column(
      children: [
        Text(
          count.toString(),
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(color: Colors.grey)),
      ],
    );
  }

  Widget _buildBioSliver(BuildContext context, ProfileEntity profile) {
    final bio = (profile.description?.trim().isNotEmpty ?? false)
        ? profile.description!
        : 'No bio provided.';
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Text(bio, style: Theme.of(context).textTheme.bodyMedium),
      ),
    );
  }

  Widget _buildPostsHeaderSliver() {
    return const SliverToBoxAdapter(
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: Text(
          'Posts',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
      ),
    );
  }

  Widget _buildFeedSliver(FeedViewModel feedViewModel) {
    final feedType = feedViewModel.feedConfig.type;
    return BlocProvider<FeedViewModel>.value(
      value: feedViewModel,
      child: switch (feedType) {
        // TODO: Sectional Feed NOT implemented in domain and infrastructure layer, AND not implemented in backend
        FeedType.sectionalFeed => const SliverSectionalFeedView(),
        FeedType.gridFeed => const SliverGridFeedView(),
        FeedType.listFeed => throw UnimplementedError(),
      },
    );
  }
}
