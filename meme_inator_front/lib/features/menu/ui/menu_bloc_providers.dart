import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/menu/ui/viewmodels/menu_cubit.dart';

final List<BlocProvider<dynamic>> menuBlocProviders = [
  BlocProvider<MenuCubit>(
    create: (context) => MenuCubit(),
  ),
];
