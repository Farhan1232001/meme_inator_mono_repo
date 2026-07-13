// lib/features/home/home_bloc_providers.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/feeds/feeds_bloc_providers.dart';
import 'package:meme_inator_front/features/menu/ui/menu_bloc_providers.dart';

final List<BlocProvider<dynamic>> homeBlocProviders = [

  ...feedsBlocProviders,
  ...menuBlocProviders
];
