import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:meme_inator_front/features/feeds/ui/widgets/post_page_view_widget.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

/// Full-screen paged view of posts, allowing swipe to next/previous.
///
/// Uses a [PageController] as controller to navigate pages, and listens
/// to [PagingController] for data and pagination events.
/// PostPageView uses KeyType so that int and string can work as keys;
/// regular pagination uses int as key, and cursor pagination
/// uses string (url) for key
class PostPageViewScreen<KeyType> extends StatefulWidget {
  final PagingController<KeyType, PostEntity> pagingController;
  final int initialIndex;

  const PostPageViewScreen({
    super.key,
    required this.pagingController,
    required this.initialIndex,
  });

  @override
  State<PostPageViewScreen<KeyType>> createState() =>
      _PostPageViewScreenState();
}

class _PostPageViewScreenState<KeyType>
    extends State<PostPageViewScreen<KeyType>> {
  late final PageController _pageController;
  late int _currentPageIndex;

  @override
  void initState() {
    super.initState();
    _currentPageIndex = widget.initialIndex;
    _pageController = PageController(initialPage: _currentPageIndex);
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  // ==================== MAIN BUILD ====================

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: true,
      onPopInvokedWithResult: (didPop, result) {
        if (didPop) return;
        // Custom pop logic only if needed
        Navigator.of(context).pop(_currentPageIndex);
      },
      child: ValueListenableBuilder<PagingState<KeyType, PostEntity>>(
        valueListenable: widget.pagingController,
        builder: (context, state, _) {
          final posts = state.items ?? [];
          final currentPost =
              (posts.isNotEmpty && _currentPageIndex < posts.length)
              ? posts[_currentPageIndex]
              : null;

          return PlatformScaffold(
            backgroundColor: Colors.black,
            appBar: _buildAppBar(currentPost),
            body: _buildContent(state),
          );
        },
      ),
    );
  }
  // ==================== MAIN CONTENT BUILDER ====================

  Widget _buildContent(PagingState<KeyType, PostEntity> state) {
    final posts = state.items ?? [];
    final currentPost = (posts.isNotEmpty && _currentPageIndex < posts.length)
        ? posts[_currentPageIndex]
        : null;

    Widget content;

    if (state.isLoading && posts.isEmpty) {
      content = _buildLoadingIndicator();
    } else if (state.error != null && posts.isEmpty) {
      content = _buildErrorIndicator();
    } else {
      content = _buildPagedPageView(state, posts);
    }

    return Column(
      children: [
        Expanded(child: content),
        if (currentPost != null) _buildFooter(currentPost),
      ],
    );
  }
  // ==================== FOOTER BUILDER ====================

  Widget _buildFooter(PostEntity currentPost) {
    return SafeArea(
      top: false,
      bottom: true,
      child: Container(
        color: Colors.black,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: Row(
          children: [
            PlatformText(
              'Author: ${currentPost.authorId}',
              style: const TextStyle(color: Colors.white70),
            ),
            const Spacer(),
            PlatformText(
              currentPost.createdOn.toString(),
              style: const TextStyle(color: Colors.white38),
            ),
          ],
        ),
      ),
    );
  }

  // ==================== POP HANDLING ====================

  /// Intercepts pop to return [_currentPageIndex] to caller.
  bool _canPop(bool didPop, dynamic result) {
    if (didPop) Navigator.of(context).maybePop(_currentPageIndex);
    return false;
  }

  // ==================== APP BAR BUILDERS ====================

  Widget _buildBackButton() {
    return PlatformIconButton(
      materialIcon: const Icon(Icons.arrow_back, color: Colors.white),
      cupertinoIcon: const Icon(CupertinoIcons.back, color: Colors.white),
      onPressed: () => _canPop(true, null),
    );
  }

  Widget _buildShareButton() {
    return PlatformIconButton(
      materialIcon: const Icon(Icons.share, color: Colors.white),
      cupertinoIcon: const Icon(CupertinoIcons.share, color: Colors.white),
      onPressed: () {
        /* TODO */
      },
    );
  }

  Widget _buildCommentButton() {
    return PlatformIconButton(
      materialIcon: const Icon(Icons.chat_bubble_outline, color: Colors.white),
      cupertinoIcon: const Icon(
        CupertinoIcons.chat_bubble,
        color: Colors.white,
      ),
      onPressed: () {
        /* TODO */
      },
    );
  }

  Widget _buildLikeRow(PostEntity? currentPost) {
    return Row(
      children: [
        PlatformIconButton(
          materialIcon: const Icon(
            Icons.thumb_up_alt_outlined,
            color: Colors.white,
          ),
          cupertinoIcon: const Icon(
            CupertinoIcons.hand_thumbsup,
            color: Colors.white,
          ),
          onPressed: () {
            /* TODO */
          },
        ),
        SizedBox(
          width: 44,
          child: Center(
            child: PlatformText(
              '${currentPost?.likesCount ?? 0}',
              style: const TextStyle(color: Colors.white),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildDislikeRow(PostEntity? currentPost) {
    return Row(
      children: [
        PlatformIconButton(
          materialIcon: const Icon(
            Icons.thumb_down_alt_outlined,
            color: Colors.white,
          ),
          cupertinoIcon: const Icon(
            CupertinoIcons.hand_thumbsdown,
            color: Colors.white,
          ),
          onPressed: () {
            /* TODO */
          },
        ),
        SizedBox(
          width: 44,
          child: Center(
            child: PlatformText(
              '${currentPost?.dislikesCount ?? 0}',
              style: const TextStyle(color: Colors.white),
            ),
          ),
        ),
      ],
    );
  }

  List<Widget> _buildMaterialAppBarActions(PostEntity? currentPost) {
    return [
      _buildShareButton(),
      _buildCommentButton(),
      _buildLikeRow(currentPost),
      _buildDislikeRow(currentPost),
    ];
  }

  Widget _buildCupertinoAppBarTrailing(PostEntity? currentPost) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        _buildShareButton(),
        _buildCommentButton(),
        _buildLikeRow(currentPost),
        _buildDislikeRow(currentPost),
      ],
    );
  }

  PlatformAppBar _buildAppBar(PostEntity? currentPost) {
    return PlatformAppBar(
      backgroundColor: Colors.black,
      leading: _buildBackButton(),
      material: (_, __) => MaterialAppBarData(
        actions: _buildMaterialAppBarActions(currentPost),
      ),
      cupertino: (_, __) => CupertinoNavigationBarData(
        trailing: _buildCupertinoAppBarTrailing(currentPost),
      ),
    );
  }

  // ==================== CONTENT BUILDERS ====================

  Widget _buildLoadingIndicator() {
    final theme = Theme.of(context);
    return Center(
      child: PlatformCircularProgressIndicator(
        material: (_, __) => MaterialProgressIndicatorData(
          color: theme.colorScheme.primary,
        ),
      ),
    );
  }

  Widget _buildErrorIndicator() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          PlatformText('😢 Failed to load.'),
          const SizedBox(height: 12),
          PlatformElevatedButton(
            onPressed: widget.pagingController.fetchNextPage,
            child: PlatformText('Retry'),
          ),
        ],
      ),
    );
  }

  Widget _buildNewPageProgressIndicator() {
    final theme = Theme.of(context);
    return Center(
      child: PlatformCircularProgressIndicator(
        material: (_, __) => MaterialProgressIndicatorData(
          color: theme.colorScheme.primary,
        ),
      ),
    );
  }

  Widget _buildNewPageErrorIndicator() {
    return Center(
      child: PlatformElevatedButton(
        onPressed: widget.pagingController.fetchNextPage,
        child: PlatformText('Retry'),
      ),
    );
  }

  Widget _buildPagedPageView(
    PagingState<KeyType, PostEntity> state,
    List<PostEntity> posts,
  ) {
    final theme = Theme.of(context);

    return PagedPageView<KeyType, PostEntity>(
      pageController: _pageController,
      state: state,
      fetchNextPage: widget.pagingController.fetchNextPage,
      scrollDirection: Axis.vertical,
      onPageChanged: (index) {
        setState(() => _currentPageIndex = index);
        if (index >= posts.length - 3) {
          widget.pagingController.fetchNextPage();
        }
      },
      builderDelegate: PagedChildBuilderDelegate<PostEntity>(
        itemBuilder: (context, post, index) => PostPageViewWidget(post: post),
        newPageProgressIndicatorBuilder: (_) =>
            _buildNewPageProgressIndicator(),
        newPageErrorIndicatorBuilder: (_) => _buildNewPageErrorIndicator(),
      ),
    );
  }
}
