// /lib/features/home/home_routes.dart
import 'package:go_router/go_router.dart';
import 'package:meme_inator_front/features/auth/ui/pages/login_page.dart';
import 'package:meme_inator_front/features/feeds/feeds_routes.dart';
import 'package:meme_inator_front/features/home/ui/pages/home_page.dart';
import 'package:meme_inator_front/features/notifications/ui/pages/notifications_page.dart';
import 'package:meme_inator_front/features/profiles/ui/pages/profile_page.dart';
import 'package:meme_inator_front/features/registration/ui/pages/registration_page.dart';

/// Routes related to Home feature
final List<GoRoute> homeRoutes = [
  GoRoute(
    path: '/home',
    name: 'home',
    builder: (context, state) => const HomePage(),
  ),
  GoRoute(
    path: '/login',
    name: 'login',
    builder: (context, state) => const LoginPage(),
  ),
  GoRoute(
    path: '/register',
    name: 'register',
    builder: (context, state) => const RegisterPage(),
  ),
  GoRoute(
    path: '/profile',
    name: 'profile',
    builder: (context, state) => const ProfilePage(profileOwnerUserId: '019d5606-d99d-71c4-9001-80780832e143', currentUserId: null,),
  ),
    GoRoute(
    path: '/notifications',
    name: 'notifications',
    builder: (context, state) => const NotificationsPage(),
  ),
  // Include feeds routes
  ...feedsRoutes,
];
