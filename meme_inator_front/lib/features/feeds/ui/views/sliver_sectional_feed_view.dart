// lib/features/feeds/ui/views/sliver_sectional_feed_view.dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:intl/intl.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/feed_states.dart';
import 'package:meme_inator_front/features/feeds/ui/custom_infinite_scroll_pagination_pkg/paged/paged_sliver_sectioned_grid.dart';
import 'package:meme_inator_front/features/feeds/ui/custom_infinite_scroll_pagination_pkg/paged/paged_sectioned_child_builder_delegate.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';
import 'package:meme_inator_front/features/profiles/ui/viewmodels/profile_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/widgets/feed_tile_widget.dart';

/// Sliver version of the sectional feed view. Designed to be placed inside a
/// CustomScrollView (like a profile page) with other slivers.
class SliverSectionalFeedView extends StatelessWidget {
  const SliverSectionalFeedView({super.key});

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
        // Haptic feedback on feed switching
        BlocListener<FeedViewModel, FeedState>(
          listenWhen: (previous, current) => current is FeedSwitching,
          listener: (context, state) async {
            await HapticFeedback.lightImpact();
          },
        ),
      ],
      child: _SliverSectionalFeedContent(),
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

class _SliverSectionalFeedContent extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final profileViewModel = context.watch<ProfileViewModel>();
    // ✅ Clear the repository to ensure fresh cursor (same as grid feed)
    final feedViewModel = profileViewModel.feedViewModel..clearFeedRepository();
    final pagingController = feedViewModel.pagingController;

    // Show loading indicator while switching feed types
    if (feedViewModel.state is FeedSwitching) {
      return const SliverFillRemaining(
        child: Center(
          child: PlatformCircularProgressIndicator(),
        ),
      );
    }

    return ValueListenableBuilder(
      valueListenable: pagingController,
      builder: (context, state, child) {
        // ✅ Trigger initial fetch if needed (handles cases where auto-fetch doesn't fire)
        if ((state.pages == null || state.pages!.isEmpty) &&
            state.status != PagingStatus.loadingFirstPage &&
            state.status != PagingStatus.firstPageError) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            pagingController.fetchNextPage();
          });
        }

        return PagedSliverSectionList<String, PostEntity>(
          state: state,
          fetchNextPage: pagingController.fetchNextPage,
          builderDelegate: PagedSectionedChildBuilderDelegate<String, PostEntity>(
            sectionBuilder: (context, section, index) {
              final title = _getSectionHeaderText(
                section.isNotEmpty ? section.first.createdOn ?? DateTime.now() : DateTime.now(),
                index,
              );
              return _buildSectionContent(context, section, title);
            },
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
                  const Text('😢 Could not load sectional posts.\nServers in the cloud may be down :{'),
                  const SizedBox(height: 12),
                  PlatformElevatedButton(
                    onPressed: () async {
                      await HapticFeedback.lightImpact();
                      pagingController.refresh();
                    },
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [Icon(Icons.refresh), SizedBox(width: 8), Text('Retry')],
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
                  children: [Icon(Icons.refresh), SizedBox(width: 8), Text('Retry')],
                ),
              ),
            ),
            noItemsFoundIndicatorBuilder: (_) => const Center(child: Text('No posts found.')),
            noMoreItemsIndicatorBuilder: (_) => const Padding(
              padding: EdgeInsets.all(16.0),
              child: Center(child: Text("You've reached the end.")),
            ),
          ),
          addAutomaticKeepAlives: true,
          addRepaintBoundaries: true,
          addSemanticIndexes: true,
          shrinkWrapFirstPageIndicators: false,
        );
      },
    );
  }

  Widget _buildSectionContent(
    BuildContext context,
    List<PostEntity> section,
    String title,
  ) {
    final theme = Theme.of(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(
            title,
            style: theme.textTheme.bodySmall,
          ),
        ),
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3,
            crossAxisSpacing: 1,
            mainAxisSpacing: 1,
            childAspectRatio: 1.0,
          ),
          itemCount: section.length,
          itemBuilder: (context, index) {
            return FeedTileWidget(
              post: section[index],
              flatIndex: index,
            );
          },
        ),
        const Divider(),
      ],
    );
  }

  String _getSectionHeaderText(DateTime createdOn, int index) {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final createdDate = DateTime(
      createdOn.year,
      createdOn.month,
      createdOn.day,
    );
    final difference = today.difference(createdDate).inDays;

    final formattedDate = DateFormat.MMMMd().format(createdDate);

    if (difference == 0) {
      return 'Popular Today – $formattedDate';
    } else if (difference == 1) {
      return 'Popular Yesterday – $formattedDate';
    } else {
      return 'Popular $difference Days Ago – $formattedDate';
    }
  }
}
