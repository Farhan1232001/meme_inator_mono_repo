import 'package:flutter/widgets.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/widgets/feed_tile_widget.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

class SectionGridTileWidget<PageKeyType, ItemType> extends StatelessWidget {
  final ItemType item;
  final int sectionIndex;
  final int sectionsItemIndex;

  const SectionGridTileWidget({
    Key? key,
    required this.item,
    required this.sectionIndex,
    required this.sectionsItemIndex,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final feedViewModel = context.read<FeedViewModel>();
    final pagingController = feedViewModel.pagingController;
    
    final flatIndex = _getFlatIndex(
      sectionIndex,
      sectionsItemIndex,
      pagingController,
    );

    return FeedTileWidget(
      post: item as PostEntity,
      flatIndex: flatIndex,
      sectionIndex: sectionIndex,
      sectionItemIndex: sectionsItemIndex,
      shouldHandleScrollBack: true, // Sectional feeds need scroll-back
    );
  }

  int _getFlatIndex(
    int sectionIndex,
    int sectionsItemIndex,
    PagingController pagingController,
  ) {
    int flatIndex = 0;
    final pages = pagingController.pages!;
    for (int i = 0; i < sectionIndex; i++) {
      flatIndex += pages[i].length;
    }
    return flatIndex + sectionsItemIndex;
  }
}
// // ignore_for_file: avoid_redundant_argument_values
// // /lib/features/feeds/ui/custom_infinite_scroll_pagination_pkg/paged/section_grid_tile_widget.dart
// import 'package:flutter/material.dart';
// import 'package:flutter_bloc/flutter_bloc.dart';
// import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
// import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
// import 'package:meme_inator_front/core/utils/pair.dart';
// import 'package:meme_inator_front/features/feeds/ui/cubit/page_section_controllers_cubit.dart';
// import 'package:meme_inator_front/features/feeds/ui/cubit/section_heights_cache.dart';
// import 'package:meme_inator_front/features/feeds/ui/custom_infinite_scroll_pagination_pkg/paged/page_grid_section.dart';
// import 'package:meme_inator_front/features/feeds/ui/pages/post_page_view_screen.dart';
// import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
// import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';
// import 'package:meme_inator_front/features/post/ui/widgets/post_widget.dart';
// import 'package:shimmer_animation/shimmer_animation.dart';


// /// Grid tile for a section widget
// class SectionGridTileWidget<PageKeyType, ItemType> extends StatelessWidget {
//   // TODO: Add shimmering loading effect, make sure they sync
//   static final Shimmer _shimmerLoadingTile = Shimmer(
//     duration: const Duration(seconds: 2), //Default value
//     interval: const Duration(seconds: 0), //Default value: Duration(seconds: 0)
//     color: Colors.white, //Default value
//     colorOpacity: 0, //Default value
//     enabled: true, //Default value
//     direction: const ShimmerDirection.fromLTRB(), //Default Value
//     child: Container(
//       color: const Color.fromARGB(255, 15, 1, 39),
//     ),
//   );

//   SectionGridTileWidget(
//       {Key? key,
//       required ItemType item,
//       required this.sectionsItemIndex,
//       required int sectionIndex})
//       : _item = item,
//         super(key: key) {
//     _sectionIndex = sectionIndex;
//   }

//   final ItemType _item;
//   late final int _sectionIndex; // TODO: every instance should store index
//   /// index of item within section
//   final int sectionsItemIndex;

//   @override
//   Widget build(BuildContext context) {
//         final feedViewModel = context.read<FeedViewModel>();

//       final pagingController = feedViewModel.pagingController;
//         final listController = feedViewModel.listController;


//         final cache = context.read<SectionHeightsCacheCubit>();

//         return GestureDetector(
//           onTap: () {
//             // find index of pages given sectionIndex and index (index within section)
//             // Problem: You have a 2D list, where inner lists vary in size, (pages). Given sectionIndex (pageIndex) and index (index of post for a page), find indexFlat to find that particular post if the 2D array is fallatened.
//             final flatIndex = getFlatIndex(
//               _sectionIndex,
//               sectionsItemIndex,
//               pagingController,
//             );
//             // When user taps on tile, it takes user to the PostPageViewScreen
//             Navigator.of(context)
//                 .push(
//               platformPageRoute(
//                 context: context,
//                 builder: (_) => PostPageViewScreen(
//                   pagingController: pagingController,
//                   initialIndex: flatIndex,
//                 ),
//               ),
//             )
//                 .then((returnedPageIndex) {
//               // func run when what was pushed is popped off
//               if (returnedPageIndex is int) {
//                 scrollToSection(
//                   returnedPageIndex,
//                   listController,
//                   pagingController,
//                   cache,
//                 );
//               }
//             });
//           },
//           child: PlatformWidget(
//             // TODO: Why the heck do i have GridTile?
//             cupertino: (_, __) => GridTile(
//               child: PostWidget(post: _item as PostEntity),
//             ),
//             material: (_, __) => GridTile(
//               child: PostWidget(post: _item as PostEntity),
//             ),
//           ),
//         );


//   }
  
//   /// Scrolls the ListView to ensure the tapped section is visible, only if the Post is not already in view.
//   void scrollToSection(
//       int flatIndex,
//       ScrollController listScrollController,
//       PagingController pagingController,
//       SectionHeightsCacheCubit sectionHeightsCache) {
//     if (!listScrollController.hasClients) return;

//     int sectionIndex = 0;
//     int localIndex = 0;
//     final pair = nonFlatIndexFromFlat(flatIndex, pagingController);
//     if (pair != null) {
//       sectionIndex = pair.first;
//       localIndex = pair.second;
//     }

//     final postHeight = PostWidget.height;
//     final cache = sectionHeightsCache.sectionHeightsList;

//     // heights in pixels
//     final cumulatedSectionHeights =
//         sectionHeightsCache.getCumulatedHeight(0, sectionIndex);
//     final cumulatedPostHeights = (localIndex /
//                 PageGridSection.getCrossAxisCount)
//             .floor() *
//         postHeight; // TODO: use PageGridSection.getCrossAxisCount not hardcode 3

//     final targetHeight = cumulatedSectionHeights! + cumulatedPostHeights;

//     // Only scroll if target is not already visible
//     final position = listScrollController.position;
//     final viewStart = position.pixels;
//     final viewEnd = position.pixels + position.viewportDimension;
//     // for edge case: int mid = a + (b - a) / 2;
//     final targetOffset =
//         targetHeight - (position.viewportDimension / 2) + (postHeight / 2);

//     // Check if the target post is within the current viewport
//     final bool isPostVisible =
//         (targetHeight < viewEnd) && ((targetHeight + postHeight) > viewStart);

//     if (!isPostVisible) {
//       listScrollController.jumpTo(targetOffset.clamp(
//         position.minScrollExtent,
//         position.maxScrollExtent,
//       ));
//     }
//   }

//   /// Given a flatIndex, returns a Pair<int, int> (sectionIndex, localIndex) such that
//   /// pages[sectionIndex][localIndex] corresponds to the item at flatIndex in the flattened list.
//   /// Returns null if flatIndex is out of bounds.
//   Pair<int, int>? nonFlatIndexFromFlat(
//       int flatIndex, PagingController pagingController) {
//     final pages = pagingController.pages;
//     if (pages == null) return null;

//     int runningTotal = 0;
//     for (int sectionIndex = 0; sectionIndex < pages.length; sectionIndex++) {
//       final sectionLength = pages[sectionIndex].length;
//       if (flatIndex < runningTotal + sectionLength) {
//         return Pair(sectionIndex, flatIndex - runningTotal);
//       }
//       runningTotal += sectionLength;
//     }
//     return null; // flatIndex out of bounds
//   }

//   /// Gets flatIndex of _pagingController's pages : List<List<PostItem>> given sectionId & localIndex of section grid.
//   /// Used to find initial index to pass in as arg when pushing PostPageViewScreen onto Navigator stack.
//   ///
//   /// Problem method solves:
//   ///   You have a 2D list, where inner lists vary in size, (pages).
//   ///   Given sectionIndex (pagIndex) and index (index of post for a page),
//   ///   find indexFlat to find that particular post if the 2D array is flattened.
//   int getFlatIndex(int sectionIndex, int sectionsItemIndex,
//       PagingController pagingController) {
//     int flatIndex = 0;
//     final pages = pagingController.pages!;
//     for (int i = 0; i < sectionIndex; i++) {
//       flatIndex += pages[i].length;
//     }
//     return flatIndex + sectionsItemIndex;
//   }



//   // Widget _build(BuildContext context) {
//   //   return BlocBuilder<SectionalFeedControllersCubit, PageSectionControllersState>(
//   //     builder: (context, state) {
//   //       final pagingController = state.pagingController;
//   //       final listController = state.listController;

//   //       if (pagingController == null || listController == null) {
//   //         // return _shimmerLoadingTile;
//   //         return const SizedBox.shrink();
//   //       }

//   //       final cache = context.read<SectionHeightsCacheCubit>();

//   //       return GestureDetector(
//   //         onTap: () {
//   //           // find index of pages given sectionIndex and index (index within section)
//   //           // Problem: You have a 2D list, where inner lists vary in size, (pages). Given sectionIndex (pageIndex) and index (index of post for a page), find indexFlat to find that particular post if the 2D array is fallatened.
//   //           final flatIndex = getFlatIndex(
//   //             _sectionIndex,
//   //             sectionsItemIndex,
//   //             pagingController,
//   //           );
//   //           // When user taps on tile, it takes user to the PostPageViewScreen
//   //           Navigator.of(context)
//   //               .push(
//   //             platformPageRoute(
//   //               context: context,
//   //               builder: (_) => PostPageViewScreen(
//   //                 pagingController: pagingController,
//   //                 initialIndex: flatIndex,
//   //               ),
//   //             ),
//   //           )
//   //               .then((returnedPageIndex) {
//   //             // func run when what was pushed is popped off
//   //             if (returnedPageIndex is int) {
//   //               scrollToSection(
//   //                 returnedPageIndex,
//   //                 listController,
//   //                 pagingController,
//   //                 cache,
//   //               );
//   //             }
//   //           });
//   //         },
//   //         child: PlatformWidget(
//   //           // TODO: Why the heck do i have GridTile?
//   //           cupertino: (_, __) => GridTile(
//   //             child: PostWidget(post: _item as PostEntity),
//   //           ),
//   //           material: (_, __) => GridTile(
//   //             child: PostWidget(post: _item as PostEntity),
//   //           ),
//   //         ),
//   //       );
//   //     },
//   //   );
//   // }

// }
