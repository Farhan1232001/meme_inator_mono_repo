import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';
import 'package:meme_inator_front/features/registration/domain/repositories/iregistration_repo.dart';
import 'package:meme_inator_front/features/registration/ui/viewmodels/registration_viewmodel.dart';

final List<BlocProvider<dynamic>> registrationBlocProviders = [
  BlocProvider<RegistrationViewModel>(
    create: (context) => RegistrationViewModel(
      repository: GetIt.instance.get<IRegistrationRepository>(),
      authRepository: GetIt.instance.get<IAuthRepository>(),
    ),
  ),
];
