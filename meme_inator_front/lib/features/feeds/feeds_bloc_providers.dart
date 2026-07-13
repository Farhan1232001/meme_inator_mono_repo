// feeds_bloc_providers.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/section_heights_cache.dart';


final List<BlocProvider<dynamic>> feedsBlocProviders = [
  
  // Section Heights Cache Cubit
  // Used by PageGridSection. and SectionGridTileWidget classes. 
  BlocProvider<SectionHeightsCacheCubit>(
    create: (context) => SectionHeightsCacheCubit(),
  ),
  
];
