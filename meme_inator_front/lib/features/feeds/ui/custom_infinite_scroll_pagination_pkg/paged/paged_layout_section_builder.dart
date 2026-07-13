import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:infinite_scroll_pagination/src/defaults/first_page_error_indicator.dart';
import 'package:infinite_scroll_pagination/src/defaults/first_page_progress_indicator.dart';
import 'package:infinite_scroll_pagination/src/defaults/new_page_error_indicator.dart';
import 'package:infinite_scroll_pagination/src/defaults/new_page_progress_indicator.dart';
import 'package:infinite_scroll_pagination/src/defaults/no_items_found_indicator.dart';
import 'package:meme_inator_front/features/feeds/ui/custom_infinite_scroll_pagination_pkg/paged/paged_sectioned_child_builder_delegate.dart';
import 'package:sliver_tools/sliver_tools.dart';

/// Called to request a new page of data, meant to be in a PageGridSection widget.
typedef NextPageSectionCallback = VoidCallback;

typedef CompletedListingBuilder = Widget Function(
  BuildContext context,
  IndexedWidgetBuilder itemWidgetBuilder,
  int itemCount,
  WidgetBuilder? noMoreItemsIndicatorBuilder,
);

typedef ErrorListingBuilder = Widget Function(
  BuildContext context,
  IndexedWidgetBuilder itemWidgetBuilder,
  int itemCount,
  WidgetBuilder newPageErrorIndicatorBuilder,
);

typedef LoadingListingBuilder = Widget Function(
  BuildContext context,
  IndexedWidgetBuilder itemWidgetBuilder,
  int itemCount,
  WidgetBuilder newPageProgressIndicatorBuilder,
);

/// The Flutter layout protocols supported by [PagedLayoutBuilder].
// enum PagedLayoutProtocol { sliver, box } // already defined in the infinite scroll pagination package

/// Facilitates creating infinitely scrolled paged layouts such that each page is given to builder at a time.
///
/// Combines a [PagingController] with a
/// [PagedChildBuilderDelegate] and calls the supplied
/// [loadingListingBuilder], [errorListingBuilder] or
/// [completedListingBuilder] for filling in the gaps.
///
class PagedLayoutSectionBuilder<PageKeyType, ItemType> extends StatefulWidget {
  const PagedLayoutSectionBuilder({
    required this.state,
    required this.fetchNextPage,
    required this.sectionBuilderDelegate,
    required this.loadingListingBuilder,
    required this.errorListingBuilder,
    required this.completedListingBuilder,
    required this.layoutProtocol,
    this.shrinkWrapFirstPageIndicators = false,
    super.key,
  });

  /// The paging state for this layout.
  final PagingState<PageKeyType, ItemType> state;

  /// A callback function that is triggered to request a new page of data.
  final NextPageSectionCallback fetchNextPage;

  /// The delegate for building the UI pieces of scrolling paged listings.
  final PagedSectionedChildBuilderDelegate<PageKeyType,ItemType> sectionBuilderDelegate;

  /// The builder for an in-progress listing.
  final LoadingListingBuilder loadingListingBuilder;

  /// The builder for an in-progress listing with a failed request.
  final ErrorListingBuilder errorListingBuilder;

  /// The builder for a completed listing.
  final CompletedListingBuilder completedListingBuilder;

  /// Whether the extent of the first page indicators should be determined by
  /// the contents being viewed.
  ///
  /// If the paged layout builder does not shrink wrap, then the first page
  /// indicators will expand to the maximum allowed size. If the paged layout
  /// builder has unbounded constraints, then [shrinkWrapFirstPageIndicators]
  /// must be true.
  ///
  /// Defaults to false.
  final bool shrinkWrapFirstPageIndicators;

  /// The layout protocol of the widget you're using this to build.
  ///
  /// For example, if [PagedLayoutProtocol.sliver] is specified, then
  /// [loadingListingBuilder], [errorListingBuilder], and
  /// [completedListingBuilder] have to return a Sliver widget.
  final PagedLayoutProtocol layoutProtocol;

  @override
  State<PagedLayoutSectionBuilder<PageKeyType, ItemType>> createState() =>
      _PagedLayoutSectionBuilderState<PageKeyType, ItemType>();
}

class _PagedLayoutSectionBuilderState<PageKeyType, ItemType>
    extends State<PagedLayoutSectionBuilder<PageKeyType, ItemType>> {
      
  PagingState<PageKeyType, ItemType> get _state => widget.state;

  NextPageSectionCallback get _fetchNextPage =>
      // We make sure to only schedule the fetch after the current build is done.
      // This is important to prevent recursive builds.
      () => WidgetsBinding.instance
          .addPostFrameCallback((_) => widget.fetchNextPage());

  PagedSectionedChildBuilderDelegate<PageKeyType, ItemType> get _sectionBuilderDelegate =>
      widget.sectionBuilderDelegate;

  bool get _shrinkWrapFirstPageIndicators =>
      widget.shrinkWrapFirstPageIndicators;

  PagedLayoutProtocol get _layoutProtocol => widget.layoutProtocol;

  WidgetBuilder get _firstPageErrorIndicatorBuilder =>
      _sectionBuilderDelegate.firstPageErrorIndicatorBuilder ??
      (_) => FirstPageErrorIndicator(
            onTryAgain: _fetchNextPage,
          );

  WidgetBuilder get _newPageErrorIndicatorBuilder =>
      _sectionBuilderDelegate.newPageErrorIndicatorBuilder ??
      (_) => NewPageErrorIndicator(
            onTap: _fetchNextPage,
          );

  WidgetBuilder get _firstPageProgressIndicatorBuilder =>
      _sectionBuilderDelegate.firstPageProgressIndicatorBuilder ??
      (_) => const FirstPageProgressIndicator();

  WidgetBuilder get _newPageProgressIndicatorBuilder =>
      _sectionBuilderDelegate.newPageProgressIndicatorBuilder ??
      (_) => const NewPageProgressIndicator();

  WidgetBuilder get _noItemsFoundIndicatorBuilder =>
      _sectionBuilderDelegate.noItemsFoundIndicatorBuilder ??
      (_) => const NoItemsFoundIndicator();

  WidgetBuilder? get _noMoreItemsIndicatorBuilder =>
      _sectionBuilderDelegate.noMoreItemsIndicatorBuilder;

  int get _invisibleItemsThreshold => _sectionBuilderDelegate.invisibleItemsThreshold;

  int get _itemCount => _state.pages?.length ?? 0;

  bool get _hasNextPage => _state.hasNextPage;

  /// Avoids duplicate requests on rebuilds.
  bool _hasRequestedNextPage = false;

  @override
  void initState() {
    super.initState();
    if (_state.status == PagingStatus.loadingFirstPage) {
      _fetchNextPage();
    }
  }

  @override
  void didUpdateWidget(
      covariant PagedLayoutSectionBuilder<PageKeyType, ItemType> oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.state != widget.state) {
      if (_state.status == PagingStatus.loadingFirstPage) {
        _fetchNextPage();
      } else if (_state.status == PagingStatus.ongoing) {
        _hasRequestedNextPage = false;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    // debugPrint('⚙️ PagedLayoutSectionBuilder.build() status = ${_state.status}');
    // debugPrint('PagedLayoutSectionBuilder build state\'s items: ${_state.items}');
    return _PagedLayoutAnimator(
      animateTransitions: _sectionBuilderDelegate.animateTransitions,
      transitionDuration: _sectionBuilderDelegate.transitionDuration,
      layoutProtocol: _layoutProtocol,
      child: switch (_state.status) {
        PagingStatus.loadingFirstPage => _FirstPageStatusIndicatorBuilder(
            key: const ValueKey(PagingStatus.loadingFirstPage),
            builder: _firstPageProgressIndicatorBuilder,
            shrinkWrap: _shrinkWrapFirstPageIndicators,
            layoutProtocol: _layoutProtocol,
          ),
        PagingStatus.firstPageError => _FirstPageStatusIndicatorBuilder(
            key: const ValueKey(PagingStatus.firstPageError),
            builder: _firstPageErrorIndicatorBuilder,
            shrinkWrap: _shrinkWrapFirstPageIndicators,
            layoutProtocol: _layoutProtocol,
          ),
        PagingStatus.noItemsFound => _FirstPageStatusIndicatorBuilder(
            key: const ValueKey(PagingStatus.noItemsFound),
            builder: _noItemsFoundIndicatorBuilder,
            shrinkWrap: _shrinkWrapFirstPageIndicators,
            layoutProtocol: _layoutProtocol,
          ),
        PagingStatus.ongoing => widget.loadingListingBuilder(
            context,
            // We must create this closure to close over the [itemList]
            // value. That way, we are safe if [itemList] value changes
            // while Flutter rebuilds the widget (due to animations, for
            // example.)
            (context, index) => _buildListItemWidget(
              context,
              index,
              _state.pages!, 
            ),
            _itemCount,
            _newPageProgressIndicatorBuilder,
          ),
        PagingStatus.subsequentPageError => widget.errorListingBuilder(
            context,
            (context, index) => _buildListItemWidget(
              context,
              index,
              _state.pages!,
            ),
            _itemCount,
            (context) => _newPageErrorIndicatorBuilder(context),
          ),
        PagingStatus.completed => widget.completedListingBuilder(
            context,
            (context, index) => _buildListItemWidget(
              context,
              index,
              _state.pages!,
            ),
            _itemCount,
            _noMoreItemsIndicatorBuilder,
          ),
      },
    );
  }

  /// Connects the [_pagingController] with the [_builderDelegate] in order to
  /// create a list item widget and request more items if needed.
  Widget _buildListItemWidget(
    BuildContext context,
    int index,
    List<List<ItemType>> pageList,
  ) {
    if (!_hasRequestedNextPage) {
      final maxIndex = max(0, _itemCount - 1);
      final triggerIndex = max(0, maxIndex - _invisibleItemsThreshold);

      // It is important to check whether we are past the trigger, not just at it.
      // This is because otherwise, large thresholds will place the trigger behind the user,
      // Leading to the refresh never being triggered.
      // This behaviour is okay because we make sure not to excessively request pages.
      final hasPassedTrigger = index >= triggerIndex;

      if (_hasNextPage && hasPassedTrigger) {
        _hasRequestedNextPage = true;
        _fetchNextPage();
      }
    }

    final section = pageList[index];
    return _sectionBuilderDelegate.sectionBuilder(context, section, index);
  }
}

class _PagedLayoutAnimator extends StatelessWidget {
  const _PagedLayoutAnimator({
    required this.child,
    required this.animateTransitions,
    required this.transitionDuration,
    required this.layoutProtocol,
  });

  final Widget child;
  final bool animateTransitions;
  final Duration transitionDuration;
  final PagedLayoutProtocol layoutProtocol;

  @override
  Widget build(BuildContext context) {
    if (!animateTransitions) return child;
    return switch (layoutProtocol) {
      PagedLayoutProtocol.sliver => SliverAnimatedSwitcher(
          duration: transitionDuration,
          child: child,
        ),
      PagedLayoutProtocol.box => AnimatedSwitcher(
          duration: transitionDuration,
          child: child,
        ),
    };
  }
}

class _FirstPageStatusIndicatorBuilder extends StatelessWidget {
  const _FirstPageStatusIndicatorBuilder({
    super.key,
    required this.builder,
    required this.layoutProtocol,
    this.shrinkWrap = false,
  });

  final WidgetBuilder builder;
  final bool shrinkWrap;
  final PagedLayoutProtocol layoutProtocol;

  @override
  Widget build(BuildContext context) {
    return switch (layoutProtocol) {
      PagedLayoutProtocol.sliver => shrinkWrap
          ? SliverToBoxAdapter(child: builder(context))
          : SliverFillRemaining(
              hasScrollBody: false,
              child: builder(context),
            ),
      PagedLayoutProtocol.box =>
        shrinkWrap ? builder(context) : Center(child: builder(context)),
    };
  }
}
