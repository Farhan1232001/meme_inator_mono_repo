// lib/features/feeds/ui/widgets/feed_tile_widget.dart

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/feed_states.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/section_heights_cache.dart';
import 'package:meme_inator_front/features/feeds/ui/pages/post_page_view_screen.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';
import 'package:meme_inator_front/features/post/ui/widgets/post_widget.dart';
import 'package:meme_inator_front/core/utils/pair.dart';

/// A unified feed tile widget that works for both grid and sectional feeds.
/// 
/// Handles navigation to PostPageViewScreen and optional scroll-back behavior
/// for sectional feeds. Platform-aware with Material and Cupertino styling.
class FeedTileWidget extends StatelessWidget {
  final PostEntity post;
  final int flatIndex;
  final int? sectionIndex;
  final int? sectionItemIndex;
  final VoidCallback? onTap;
  final bool shouldHandleScrollBack;

  const FeedTileWidget({
    Key? key,
    required this.post,
    required this.flatIndex,
    this.sectionIndex,
    this.sectionItemIndex,
    this.onTap,
    this.shouldHandleScrollBack = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final feedViewModel = context.read<FeedViewModel>();
    final pagingController = feedViewModel.pagingController;
    final feedState = feedViewModel.state;
    
    // Determine if this is a sectional feed
    final isSectionalFeed = feedState is FeedLoadedState && 
        feedState.type == FeedType.sectionalFeed;

    return GestureDetector(
      onTap: onTap ?? () => _handleTap(context, pagingController, isSectionalFeed),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(4),
        child: PlatformWidget(
          material: (_, __) => _buildMaterialTile(),
          cupertino: (_, __) => _buildCupertinoTile(),
        ),
      ),
    );
  }

  Widget _buildMaterialTile() {
    return GridTile(
      child: Stack(
        fit: StackFit.expand,
        children: [
          // Post image
          Image.network(
            post.thumbnailUrl ?? '',
            fit: BoxFit.cover,
            errorBuilder: (context, error, stackTrace) {
              return Container(
                color: Colors.grey[300],
                child: const Icon(
                  Icons.broken_image,
                  size: 40,
                  color: Colors.grey,
                ),
              );
            },
            loadingBuilder: (context, child, loadingProgress) {
              if (loadingProgress == null) return child;
              return Container(
                color: Colors.grey[200],
                child: const Center(
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                  ),
                ),
              );
            },
          ),
          
          // Material-specific overlay (e.g., ripple effect)
          Positioned.fill(
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () {}, // GestureDetector handles the tap
                splashColor: Colors.white.withOpacity(0.3),
                highlightColor: Colors.white.withOpacity(0.1),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCupertinoTile() {
    return GridTile(
      child: Stack(
        fit: StackFit.expand,
        children: [
          // Post image
          Image.network(
            post.thumbnailUrl ?? '',
            fit: BoxFit.cover,
            errorBuilder: (context, error, stackTrace) {
              return Container(
                color: CupertinoColors.systemGrey5,
                child: const Icon(
                  CupertinoIcons.photo_fill_on_rectangle_fill,
                  size: 40,
                  color: CupertinoColors.systemGrey,
                ),
              );
            },
            loadingBuilder: (context, child, loadingProgress) {
              if (loadingProgress == null) return child;
              return Container(
                color: CupertinoColors.systemGrey6,
                child: const Center(
                  child: CupertinoActivityIndicator(),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  // ==================== TAP HANDLING ====================

  void _handleTap(
    BuildContext context,
    PagingController<String, PostEntity> pagingController,
    bool isSectionalFeed,
  ) {
    Navigator.of(context)
        .push(
          platformPageRoute(
            context: context,
            builder: (_) => PostPageViewScreen(
              pagingController: pagingController,
              initialIndex: flatIndex,
            ),
          ),
        )
        .then((returnedIndex) {
          if (shouldHandleScrollBack && 
              returnedIndex is int && 
              isSectionalFeed) {
            _scrollToSectionAfterReturn(
              context,
              returnedIndex,
              pagingController,
            );
          }
        });
  }

  // ==================== SCROLL BACK HANDLING (for sectional feeds) ====================

  void _scrollToSectionAfterReturn(
    BuildContext context,
    int returnedFlatIndex,
    PagingController<String, PostEntity> pagingController,
  ) {
    if (sectionIndex == null || sectionItemIndex == null) return;

    final feedViewModel = context.read<FeedViewModel>();
    final listController = feedViewModel.listController;
    final cache = context.read<SectionHeightsCacheCubit>();

    if (!listController.hasClients) return;

    _scrollToSection(
      returnedFlatIndex,
      listController,
      pagingController,
      cache,
    );
  }

  void _scrollToSection(
    int flatIndex,
    ScrollController listScrollController,
    PagingController pagingController,
    SectionHeightsCacheCubit sectionHeightsCache,
  ) {
    if (!listScrollController.hasClients) return;

    int sectionIndex = 0;
    int localIndex = 0;
    final pair = _nonFlatIndexFromFlat(flatIndex, pagingController);
    if (pair != null) {
      sectionIndex = pair.first;
      localIndex = pair.second;
    }

    final postHeight = PostWidget.height;
    const crossAxisCount = 3; // This should come from feed config

    // heights in pixels
    final cumulatedSectionHeights =
        sectionHeightsCache.getCumulatedHeight(0, sectionIndex);
    final cumulatedPostHeights = (localIndex / crossAxisCount).floor() * postHeight;

    if (cumulatedSectionHeights == null) return;

    final targetHeight = cumulatedSectionHeights + cumulatedPostHeights;

    // Only scroll if target is not already visible
    final position = listScrollController.position;
    final viewStart = position.pixels;
    final viewEnd = position.pixels + position.viewportDimension;
    
    final targetOffset =
        targetHeight - (position.viewportDimension / 2) + (postHeight / 2);

    // Check if the target post is within the current viewport
    final bool isPostVisible =
        (targetHeight < viewEnd) && ((targetHeight + postHeight) > viewStart);

    if (!isPostVisible) {
      listScrollController.jumpTo(targetOffset.clamp(
        position.minScrollExtent,
        position.maxScrollExtent,
      ));
    }
  }

  /// Given a flatIndex, returns a Pair<int, int> (sectionIndex, localIndex) such that
  /// pages[sectionIndex][localIndex] corresponds to the item at flatIndex in the flattened list.
  /// Returns null if flatIndex is out of bounds.
  Pair<int, int>? _nonFlatIndexFromFlat(
    int flatIndex,
    PagingController pagingController,
  ) {
    final pages = pagingController.pages;
    if (pages == null) return null;

    int runningTotal = 0;
    for (int sectionIdx = 0; sectionIdx < pages.length; sectionIdx++) {
      final sectionLength = pages[sectionIdx].length;
      if (flatIndex < runningTotal + sectionLength) {
        return Pair(sectionIdx, flatIndex - runningTotal);
      }
      runningTotal += sectionLength;
    }
    return null;
  }
}