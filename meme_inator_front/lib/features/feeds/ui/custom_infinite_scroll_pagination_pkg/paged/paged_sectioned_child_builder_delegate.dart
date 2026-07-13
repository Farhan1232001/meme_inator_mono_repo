import 'package:flutter/widgets.dart';

typedef SectionedItemWidgetBuilder<PageKeyType, ItemType> = Widget Function(
  BuildContext context,
  List<ItemType> itemsToBeInASection,
  int sectionIndex,
);

/// Supplies builders for the visual components of paged views.
///
/// The generic type [ItemType] must be specified in order to properly identify
/// the list item's type.
class PagedSectionedChildBuilderDelegate<PageKeyType, ItemType> {
  const PagedSectionedChildBuilderDelegate({
    required this.sectionBuilder,
    this.firstPageErrorIndicatorBuilder,
    this.newPageErrorIndicatorBuilder,
    this.firstPageProgressIndicatorBuilder,
    this.newPageProgressIndicatorBuilder,
    this.noItemsFoundIndicatorBuilder,
    this.noMoreItemsIndicatorBuilder,
    this.animateTransitions = false,
    this.transitionDuration = const Duration(milliseconds: 250),
    this.invisibleItemsThreshold = 3,
  });

  /// The builder for list items IN A section.
  final SectionedItemWidgetBuilder<PageKeyType, ItemType> sectionBuilder;

  /// The builder for the first page's error indicator.
  final WidgetBuilder? firstPageErrorIndicatorBuilder;

  /// The builder for a new page's error indicator.
  final WidgetBuilder? newPageErrorIndicatorBuilder;

  /// The builder for the first page's progress indicator.
  final WidgetBuilder? firstPageProgressIndicatorBuilder;

  /// The builder for a new page's progress indicator.
  final WidgetBuilder? newPageProgressIndicatorBuilder;

  /// The builder for a no items list indicator.
  final WidgetBuilder? noItemsFoundIndicatorBuilder;

  /// The builder for an indicator that all items have been fetched.
  final WidgetBuilder? noMoreItemsIndicatorBuilder;

  /// Whether status transitions should be animated.
  final bool animateTransitions;

  /// The duration of animated transitions when [animateTransitions] is `true`.
  final Duration transitionDuration;

  /// The number of remaining invisible items that should trigger a new fetch.
  final int invisibleItemsThreshold;
}
