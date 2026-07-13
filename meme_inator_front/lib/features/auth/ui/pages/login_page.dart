import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/auth/ui/viewmodels/auth_viewmodel.dart';
import 'package:meme_inator_front/features/auth/ui/views/login_view.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider.value(
      value: context.read<AuthViewModel>(),
      child: const LoginView(),
    );
  }
}