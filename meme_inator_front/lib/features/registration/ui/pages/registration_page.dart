import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/registration/registration_bloc_providers.dart';
import 'package:meme_inator_front/features/registration/ui/views/register_view.dart';

class RegisterPage extends StatelessWidget {
  const RegisterPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: registrationBlocProviders,
      child: const RegisterView(),
    );
  }
}
