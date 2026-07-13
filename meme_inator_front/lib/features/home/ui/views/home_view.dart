// lib/features/home/ui/views/home_view.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/views/grid_feed_view.dart';
import 'package:meme_inator_front/features/feeds/ui/views/sectional_feed_view.dart';
import 'package:meme_inator_front/features/home/ui/cubit/home_states.dart';
import 'package:meme_inator_front/features/home/ui/viewmodels/home_viewmodel.dart';
import 'package:meme_inator_front/features/home/ui/widgets/sliding_overlay.dart';
import 'package:meme_inator_front/features/menu/ui/views/menu_view.dart';

class HomeView extends StatelessWidget {
  final FeedConfig _selectedFeedConfig;
  final bool _isMenuOpen;

  const HomeView({
    super.key,
    required FeedConfig currentFeedConfig,
    required bool isMenuOpen,
  }) : _selectedFeedConfig = currentFeedConfig,
       _isMenuOpen = isMenuOpen;

  @override
  Widget build(BuildContext context) {
    return SlidingOverlay(
        base: _feedViewRouter(context), 
        overlay: MenuView(
          onSelectFeed: (config) {
            context.read<HomeViewModel>().selectFeed(config);
          },
        ),
        showOverlay: _isMenuOpen,
      );
  }

  Widget _feedViewRouter(BuildContext context) {
    final homeState = context.read<HomeViewModel>().state;
    if (homeState is! HomeLoaded) return const SizedBox.shrink();
    
    // Get feed ViewModel directly from HomeViewModel
    final currentFeedVM = context.read<HomeViewModel>().currentFeedViewModel;
    if (currentFeedVM == null) return const SizedBox.shrink();
    
    final feedType = homeState.currentFeedConfig.type;

    switch (feedType) {
      case FeedType.sectionalFeed:
        return _buildSectionFeedView(context, currentFeedVM);
      case FeedType.gridFeed:
        return _buildGridFeedView(context, currentFeedVM);
      case FeedType.listFeed:
        throw UnimplementedError('List feed not implemented yet');
    }
  }

  Widget _buildSectionFeedView(BuildContext context, FeedViewModel viewModel) {
    return BlocProvider.value(
      value: viewModel,
      child: const SectionalFeedView(),
    );
  }
  
  Widget _buildGridFeedView(BuildContext context, FeedViewModel viewModel) {
    return BlocProvider.value(
      value: viewModel,
      child: const GridFeedView(),
    );
  }
}