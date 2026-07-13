// lib/app/app_bloc_providers.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/auth/auth_bloc_providers.dart';
import 'package:meme_inator_front/features/feeds/ui/controllers/home_feed_controller.dart';
import 'package:meme_inator_front/features/home/ui/viewmodels/home_viewmodel.dart';

final List<BlocProvider<dynamic>> globalBlocProviders = [

  // Create HomeViewModel
  BlocProvider<HomeViewModel>(
    create: (context) => HomeViewModel(feedController: HomeFeedController()),
  ),

  ...authBlocProviders
];
