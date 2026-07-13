// lib/features/feeds/ui/views/grid_feed_view.dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/feed_states.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/widgets/feed_tile_widget.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

class GridFeedView extends StatelessWidget {
  const GridFeedView({super.key}); // Removed viewModel parameter - now provided via BlocProvider

  @override
  Widget build(BuildContext context) {
    // Watch the ViewModel - rebuild when state changes
    final pagingController = context.select((FeedViewModel vm) => vm.pagingController);
    final listController = context.select((FeedViewModel vm) => vm.listController);

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
                  child: PagedGridView<String, PostEntity>(
                    state: state,
                    fetchNextPage: fetchNextPage,
                    scrollController: listController,
                    physics: const AlwaysScrollableScrollPhysics(),
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 3,
                      crossAxisSpacing: 1,
                      mainAxisSpacing: 1,
                      childAspectRatio: 1.0,
                    ),
                    builderDelegate: PagedChildBuilderDelegate<PostEntity>(
                      /// TODO: Should NOT use PostWidget. 
                      itemBuilder: (context, item, index) => FeedTileWidget(
                        post: item, 
                        flatIndex: index,
                      ),
                      firstPageProgressIndicatorBuilder: (context) => const Center(
                        child: PlatformCircularProgressIndicator(),
                      ),
                      newPageProgressIndicatorBuilder: (context) => const Center(
                        child: PlatformCircularProgressIndicator(),
                      ),
                      firstPageErrorIndicatorBuilder: (context) => Center(
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
                          const Center(child: Text('No posts found.')),
                      noMoreItemsIndicatorBuilder: (context) => const Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Center(child: Text("You've reached the end.")),
                      ),
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

  void _showCriticalErrorDialog(BuildContext context, String title, String message) async {
    await showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          PlatformDialogAction(
            child: const Text('OK'),
            onPressed: () async {
              Navigator.of(context).pop();
              context.read<FeedViewModel>().handleFeedGlobalError();
            },
          ),
          PlatformDialogAction(
            child: const Text('Retry'),
            onPressed: () async {
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