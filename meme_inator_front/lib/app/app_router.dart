// lib/app/app_router.dart
import 'package:go_router/go_router.dart';
import 'package:meme_inator_front/features/home/home_routes.dart';

final GoRouter appRouter = GoRouter(
  initialLocation: '/home',
  routes: [
    ...homeRoutes
  ],
);
