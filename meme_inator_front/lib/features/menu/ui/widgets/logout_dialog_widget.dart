// features/menu/ui/widgets/logout_dialog_widget.dart
// ignore_for_file: cascade_invocations

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_events.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_states.dart';
import 'package:meme_inator_front/features/auth/ui/viewmodels/auth_viewmodel.dart';

class LogoutDialogWidget extends StatelessWidget {
  const LogoutDialogWidget({super.key});

  Future<void> show(BuildContext context) => showPlatformDialog(
        context: context,
        builder: (_) => const LogoutDialogWidget(),
      );

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<AuthViewModel, AuthState>(
      listenWhen: (previous, current) => 
          current is UnauthenticatedState || current is AuthErrorState,
      listener: (context, state) async {
        if (state is UnauthenticatedState) {
          // Success - close the logout dialog
          if (Navigator.canPop(context)) {
            Navigator.pop(context); // Close logout dialog
          }
        } else if (state is AuthErrorState) {
          // Show error dialog, then close logout dialog
          await _showErrorDialog(context, state.message);
          if (Navigator.canPop(context)) {
            Navigator.pop(context); // Close logout dialog
          }
        }
      },
      builder: (context, state) {
        final isLoading = state is AuthLoadingState;
        
        return PlatformAlertDialog(
          title: const Text('Logout Confirmation'),
          content: isLoading 
              ? const Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text('Logging out...'),
                    SizedBox(height: 16),
                    PlatformCircularProgressIndicator(),
                  ],
                )
              : const Text('Are you sure you want to logout?'),
          actions: isLoading
              ? [] // No actions while loading
              : [
                  PlatformDialogAction(
                    child: const Text('Cancel'),
                    onPressed: () => Navigator.pop(context),
                  ),
                  PlatformDialogAction(
                    child: const Text('Logout'),
                    onPressed: () {
                      context.read<AuthViewModel>().add(AuthLogoutRequestedEvent());
                    },
                  ),
                ],
        );
      },
    );
  }

  Future<void> _showErrorDialog(BuildContext context, String message) {
    return showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: const Text('Logout Failed'),
        content: Text(message),
        actions: [
          PlatformDialogAction(
            child: const Text('OK'),
            onPressed: () => Navigator.pop(context),
          ),
        ],
      ),
    );
  }
}
