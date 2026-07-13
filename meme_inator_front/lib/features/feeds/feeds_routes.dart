// lib/features/feeds/feeds_routes.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/home/ui/pages/home_page.dart';
import 'package:meme_inator_front/features/home/ui/viewmodels/home_viewmodel.dart';

/// Routes related to Feeds feature
final List<GoRoute> feedsRoutes = [
  GoRoute(
    path: '/home/:feedSlug',
    name: 'feed_detail',
    builder: (context, state) {
      // Get slug
      final feedSlug = state.pathParameters['feedSlug']!;
      // Map feedSlug to FeedConfig
      final feedConfig = FeedConfig.mapSlugToFeedConfig(feedSlug);
      // Toggle Feed
      context.read<HomeViewModel>().selectFeed(feedConfig);
      
      // Navigate back to home page with updated state
      // This will trigger a rebuild with the new feed
      return HomePage();
    },
  ),
];

