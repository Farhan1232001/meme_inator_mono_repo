// lib/features/feeds/ui/views/sectional_feed_view.dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:intl/intl.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/feed_states.dart';
import 'package:meme_inator_front/features/feeds/ui/custom_infinite_scroll_pagination_pkg/paged/paged_section_grid_view.dart';
import 'package:meme_inator_front/features/feeds/ui/custom_infinite_scroll_pagination_pkg/paged/paged_sectioned_child_builder_delegate.dart';
import 'package:meme_inator_front/features/feeds/ui/custom_infinite_scroll_pagination_pkg/paged/sectioned_grid_view.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

class SectionalFeedView extends StatelessWidget {
  const SectionalFeedView({super.key}); // Removed viewModel parameter - now provided via BlocProvider

  @override
  Widget build(BuildContext context) {
    // Watch the ViewModel - rebuild when state changes
    final pagingController = context.select((FeedViewModel vm) => vm.pagingController);
    final listController = context.select((FeedViewModel vm) => vm.listController);
    final theme = Theme.of(context);

    return MultiBlocListener(
      listeners: [
        // Listen for global feed errors (critical errors like auth failure)
        BlocListener<FeedViewModel, FeedState>(
          listenWhen: (previous, current) => current is FeedGlobalError,
          listener: (context, state) {
            if (state is FeedGlobalError) {
              final title = '${state.statusCode} ${state.staticMessage ?? ''}';
              String message = '';
              
              if (!kDebugMode) {
                message = '${state.message}\n${state.exception}';
              }
              _showCriticalErrorDialog(context, title, message);
            }
          },
        ),
        // Listen for success messages (non-critical, show as dialog)
        BlocListener<FeedViewModel, FeedState>(
          listenWhen: (previous, current) => current is FeedGlobalMessage,
          listener: (context, state) {
            if (state is FeedGlobalMessage) {
              _showInfoDialog(context, state.message);
            }
          },
        ),
        // Listen for feed switching to provide haptic feedback
        BlocListener<FeedViewModel, FeedState>(
          listenWhen: (previous, current) => current is FeedSwitching,
          listener: (context, state) async {
            await HapticFeedback.lightImpact();
          },
        ),
      ],
      child: Builder(
        builder: (context) {
          // Show a global loading indicator when switching feeds
          final feedViewModel = context.watch<FeedViewModel>();
          final feedState = feedViewModel.state;
          if (feedState is FeedSwitching) {
            return const Center(
              child: PlatformCircularProgressIndicator(),
            );
          }

          return RefreshIndicator.adaptive( 
            onRefresh: () async {
              await HapticFeedback.mediumImpact();
              await feedViewModel.refreshFeed();
            },
            child: PagingListener<String, PostEntity>(
              controller: pagingController,
              builder: (
                BuildContext context,
                PagingState<String, PostEntity> state,
                void Function() fetchNextPage,
              ) {
                return SizedBox(
                  width: MediaQuery.of(context).size.width,
                  child: PagedSectionListView<String, PostEntity>(
                    state: state,
                    fetchNextPage: fetchNextPage,
                    scrollController: listController,
                    physics: const AlwaysScrollableScrollPhysics(),
                    sectionBuilderDelegate:
                        PagedSectionedChildBuilderDelegate<String, PostEntity>(
                      sectionBuilder: (
                        BuildContext context,
                        List<PostEntity> section,
                        int index,
                      ) {
                        final title = _getSectionHeaderText(
                          section.isNotEmpty
                              ? section.first.createdOn ?? DateTime.now()
                              : DateTime.now(),
                          index,
                        );
                        return SectionedGridView<String, PostEntity>(
                          crossAxisSpacing: 0.5,
                          mainAxisSpacing: 0.5,
                          sectionIndex: index,
                          items: section,
                          header: Text(
                            title,
                            style: theme.textTheme.bodySmall,
                          ),
                          footer: const Divider(),
                        );
                      },
                      firstPageProgressIndicatorBuilder: (context) => const PlatformCircularProgressIndicator(),
                      newPageProgressIndicatorBuilder: (context) => const Center(
                        child: PlatformCircularProgressIndicator(),
                      ),
                      firstPageErrorIndicatorBuilder: (context) => Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text(
                              '😢 Could not load Popular posts.\nServers in the cloud may be down :{',
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
                      newPageErrorIndicatorBuilder: (context) => Center(
                        child: PlatformElevatedButton(
                          onPressed: () async {
                            await HapticFeedback.lightImpact();
                            fetchNextPage(); // Simply retry with same cursor
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
                      noItemsFoundIndicatorBuilder: (context) =>
                          const Center(child: Text('No popular posts found.')),
                      noMoreItemsIndicatorBuilder: (context) =>
                          const Center(child: Text('You\'ve reached the end.')),
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }

  void _showCriticalErrorDialog(BuildContext context, String title, String message) {
    showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          PlatformDialogAction(
            child: const Text('OK'),
            onPressed: () => Navigator.of(context).pop(),
          ),
          PlatformDialogAction(
            child: const Text('Retry'),
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