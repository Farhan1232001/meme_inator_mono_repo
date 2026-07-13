import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';
import 'package:meme_inator_front/features/auth/ui/viewmodels/auth_viewmodel.dart';

final List<BlocProvider<dynamic>> authBlocProviders = [
  BlocProvider<AuthViewModel>(
    create: (context) => AuthViewModel(
      authRepository: GetIt.instance.get<IAuthRepository>(),
    ),
  ),
];
