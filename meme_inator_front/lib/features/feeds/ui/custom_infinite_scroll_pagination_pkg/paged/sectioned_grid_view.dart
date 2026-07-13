// ignore_for_file: use_null_aware_elements

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/section_heights_cache.dart';
import 'package:meme_inator_front/features/feeds/ui/widgets/section_grid_tile_widget.dart';

/// Section displays contents of ONE duration window. 
/// 
/// Formally called 'PageGridSection'
class SectionedGridView<PageKeyType, ItemType> extends StatelessWidget {

  final int sectionIndex;
  final List<ItemType> items; // holds items of A page
  Widget? header;
  Widget? footer;
  int crossAxisCount;
  double crossAxisSpacing;
  double mainAxisSpacing;

  static int get getCrossAxisCount => 3;
  
  SectionedGridView({
    required this.sectionIndex,
    required this.items,
    this.header,
    this.footer,
    this.crossAxisCount = 3,
    this.crossAxisSpacing = 1.0,
    this.mainAxisSpacing = 1.0,
    super.key,
  });



  @override
  Widget build(BuildContext context) {
    final sectionHeightsCache = context.read<SectionHeightsCacheCubit>();
    if (sectionHeightsCache.getSectionHeight(sectionIndex) == null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
      final box = context.findRenderObject() as RenderBox?;
      if (box != null && box.hasSize) {
        sectionHeightsCache.setSectionHeight(sectionIndex, box.size.height);
      }
    });
    }



    int itemsIndex = 0;
    return Column(
      children: [
        if (header != null) header!,

        GridView(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: crossAxisCount,
            crossAxisSpacing: crossAxisSpacing,
            mainAxisSpacing: mainAxisSpacing,
          ),
          children: items.map((item) {
            return SectionGridTileWidget<PageKeyType, ItemType>(
              sectionIndex: sectionIndex,
              item: item,
              sectionsItemIndex: itemsIndex++,
            );
          }).toList(),
        ),

        if (footer != null) footer!,
      ]
    );
  }
}
