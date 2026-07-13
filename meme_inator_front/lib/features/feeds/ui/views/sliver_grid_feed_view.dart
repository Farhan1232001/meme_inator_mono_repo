// sliver_grid_feed_view.dart
// ignore_for_file: cascade_invocations

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/feed_states.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/widgets/feed_tile_widget.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';
import 'package:meme_inator_front/features/profiles/ui/viewmodels/profile_viewmodel.dart';

///
/// SliverGridFeedView vs GridFeedView:
///   GridFeedView wraps PagedGridView which IS A BoxScrollView that uses PagedSliverGrid.
///   SliverFeedView does NOT have BoxScrollView wrapper, and uses PagedSliverGrid directly.
///
/// When to use SliverGridFeedView?
///   You need the grid as part of a larger scrollable view (like a profile with header + grid)
///   You want the header to scroll away with the grid (common in profile designs)
///
/// When to use GridFeedView?
///   You want a standalone grid page (like a dedicated "Posts" tab)
///   The grid is the only thing on the screen
class SliverGridFeedView extends StatelessWidget {
  const SliverGridFeedView({super.key});

  @override
  Widget build(BuildContext context) {

    return MultiBlocListener(
      listeners: [
        // Feed global error listener
        BlocListener<FeedViewModel, FeedState>(
          listenWhen: (previous, current) => current is FeedGlobalError,
          listener: (context, state) {
            if (state is FeedGlobalError) {
              _showFeedErrorDialog(context, state);
            }
          },
        ),
        // Feed info message listener
        BlocListener<FeedViewModel, FeedState>(
          listenWhen: (previous, current) => current is FeedGlobalMessage,
          listener: (context, state) {
            if (state is FeedGlobalMessage) {
              _showInfoDialog(context, state.message);
            }
          },
        ),
      ],
      child: _SliverGridFeedContent(),
    );
  }

  void _showFeedErrorDialog(BuildContext context, FeedGlobalError error) {
    final title = '${error.statusCode} ${error.staticMessage ?? ''}';
    final message = error.message;
    showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          PlatformDialogAction(
            child: const Text('OK'),
            onPressed: () {
              Navigator.of(context).pop();
              context.read<FeedViewModel>().handleFeedGlobalError();
            },
          ),
        ],
      ),
    );
  }

  void _showInfoDialog(BuildContext context, String message) {
    showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: const Text('Info'),
        content: Text(message),
        actions: [
          PlatformDialogAction(
            child: const Text('OK'),
            onPressed: () => Navigator.of(context).pop(),
          ),
        ],
      ),
    );
  }
}

/// Private inner widget that contains the actual grid content
/// This ensures the BlocListeners don't interfere with the grid's own BlocBuilder/watch
class _SliverGridFeedContent extends StatelessWidget {
  
  @override
  Widget build(BuildContext context) {
    // TODO: Maybe watch FeedViewModel??? Or remove it since ValueListenableBuilder is being used, watching changes to pagingController directly. 
    final profileViewModel = context.watch<ProfileViewModel>();
    final feedViewModel = profileViewModel.feedViewModel..clearFeedRepository();
    final pagingController = feedViewModel.pagingController;
    
    // Force a rebuild when paging controller changes
    // This is the key fix - listen to the ValueNotifier directly
    return ValueListenableBuilder(
      valueListenable: pagingController,
      builder: (context, state, child) {
        // Handle feed switching state
        if (feedViewModel.state is FeedSwitching) {
          return const SliverFillRemaining(
            child: Center(
              child: PlatformCircularProgressIndicator(),
            ),
          );
        }

        return PagedSliverGrid<String, PostEntity>(
          state: state, // Use the current state from ValueListenableBuilder
          fetchNextPage: pagingController.fetchNextPage,
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3,
            crossAxisSpacing: 1,
            mainAxisSpacing: 1,
            childAspectRatio: 1.0,
          ),
          builderDelegate: PagedChildBuilderDelegate<PostEntity>(
            itemBuilder: (context, item, index) => FeedTileWidget(
              post: item,
              flatIndex: index,
            ),
            firstPageProgressIndicatorBuilder: (_) => const Center(
              child: PlatformCircularProgressIndicator(),
            ),
            newPageProgressIndicatorBuilder: (_) => const Center(
              child: PlatformCircularProgressIndicator(),
            ),
            firstPageErrorIndicatorBuilder: (_) => Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    '😢 Could not load grid posts.\nServers in the cloud may be down :{',
                  ),
                  const SizedBox(height: 12),
                  PlatformElevatedButton(
                    onPressed: () async {
                      await HapticFeedback.lightImpact();
                      pagingController.refresh();
                    },
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
            ),
            newPageErrorIndicatorBuilder: (_) => Center(
              child: PlatformElevatedButton(
                onPressed: () async {
                  await HapticFeedback.lightImpact();
                  await feedViewModel.refreshFeed();
                },
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.refresh),
                    SizedBox(width: 8),
                    Text('Retry'),
                  ],
                ),
              ),
            ),
            noItemsFoundIndicatorBuilder: (_) =>
                const Center(child: Text('No posts found.')),
            noMoreItemsIndicatorBuilder: (_) => const Padding(
              padding: EdgeInsets.all(16.0),
              child: Center(child: Text("You've reached the end.")),
            ),
          ),
          addAutomaticKeepAlives: true,
          addRepaintBoundaries: true,
          addSemanticIndexes: true,
          showNewPageProgressIndicatorAsGridChild: true,
          showNewPageErrorIndicatorAsGridChild: true,
          showNoMoreItemsIndicatorAsGridChild: true,
          shrinkWrapFirstPageIndicators: false,
        );
      },
    );
  }
}