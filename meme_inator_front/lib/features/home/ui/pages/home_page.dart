// lib/features/home/ui/pages/home_page.dart
// ignore_for_file: unnecessary_lambdas

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:go_router/go_router.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_events.dart';
import 'package:meme_inator_front/features/auth/ui/viewmodels/auth_viewmodel.dart';
import 'package:meme_inator_front/features/home/home_bloc_providers.dart';
import 'package:meme_inator_front/features/home/ui/cubit/home_states.dart';
import 'package:meme_inator_front/features/home/ui/viewmodels/home_viewmodel.dart';
import 'package:meme_inator_front/features/home/ui/views/home_view.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {

    // Check authentication status, log the User in if authenticated
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AuthViewModel>().add(
        const AuthCheckStatusRequestedEvent()
      );
    });
    
    return MultiBlocProvider(
      providers: homeBlocProviders,
      child: PlatformScaffold(
            appBar: PlatformAppBar(
              title: _selectAppBarTitle(context),
              leading: _buildMenuButton(context),
              trailingActions: _buildAppBarActions(context),
            ),
            body: _buildBody(context),
          )
    );
  }

Widget _selectAppBarTitle(BuildContext context) {
  // Use BlocBuilder to properly listen to state changes
  return BlocBuilder<HomeViewModel, HomeState>( // Define types for clarity
    builder: (context, state) {
      // The 'state' here is the current state emitted by the Bloc
      return switch (state) {
        final HomeLoaded s => Text(s.currentFeedConfig.title),
        final HomeLoading s => Text(s.targetFeedConfig.title),
        _ => const Text('Home'),
      };
    },
  );
}


  List<Widget>? _buildAppBarActions(BuildContext context) {
    return [_buildNotificationsButton(context), _buildMessagesButton(context)];
  }

  Widget _buildBody(BuildContext context) {
    return BlocBuilder<HomeViewModel, HomeState>(
      builder: (context, state) {
        // Use switch expression for cleaner, exhaustive handling
        return switch (state) {
          HomeLoading() => const CircularProgressIndicator(),
          HomeLoaded(
            currentFeedConfig: final config,
            isMenuOpen: final menuOpen
          ) =>
            HomeView(
              currentFeedConfig: config,
              isMenuOpen: menuOpen,
            ),
          HomeError(errorMsg: final msg) => Center(child: Text(msg)),
          _ => const SizedBox.shrink(),
        };
      },
    );
  }

  Widget _buildMenuButton(BuildContext context) {
    return BlocListener<HomeViewModel, HomeState>(
      listener: _listener,
      listenWhen: _listenWhen,
      child: PlatformIconButton(
        materialIcon: const Icon(Icons.menu),
        cupertinoIcon: const Icon(CupertinoIcons.bars),
        onPressed: context.watch<HomeViewModel>().toggleMenu,
      ),
    );
  }

  Widget _buildNotificationsButton(BuildContext context) {
    return BlocListener<HomeViewModel, HomeState>(
      listener: _listener,
      listenWhen: _listenWhen,
      child: PlatformIconButton(
        materialIcon: const Icon(Icons.notifications),
        cupertinoIcon: const Icon(CupertinoIcons.bell),
        onPressed: () async {
          await GoRouter.of(context).push('/notifications');
        },
      ),
    );
  }

  Widget _buildMessagesButton(BuildContext context) {
    return BlocListener<HomeViewModel, HomeState>(
      listener: _listener,
      listenWhen: _listenWhen,
      child: PlatformIconButton(
        materialIcon: const Icon(Icons.message),
        cupertinoIcon: const Icon(CupertinoIcons.chat_bubble),
        onPressed: () async {
          await GoRouter.of(context).push('/messages');
        },
      ),
    );
  }

  Future<void> _listener(BuildContext context, HomeState state) async {
    /// side-effects from state change go here
    /// ex. Navivation, snackbars/toasts, dialogs, bottomsheets, haptic feedback,
    ///   logging/analytics, imperative UI commands (scroll, focus, animation controlers)
    final prev = context.read<HomeViewModel>().previousState;

    if (prev is HomeLoaded && state is HomeLoaded) {
      if (prev.currentFeedConfig != state.currentFeedConfig) {
        await HapticFeedback.selectionClick(); // feed switched
      }

      if (prev.isMenuOpen != state.isMenuOpen) {
        await HapticFeedback.lightImpact(); // menu toggle
      }
    }

    if (state is HomeError) {
      await HapticFeedback.heavyImpact();
    }
  }

  bool _listenWhen(HomeState previous, HomeState current) {
    if (previous is HomeLoaded && current is HomeLoaded) {
      return previous.currentFeedConfig != current.currentFeedConfig ||
          previous.isMenuOpen != current.isMenuOpen;
    }

    // fire when loading → loaded
    return previous is HomeLoading && current is HomeLoaded;
  }
}
