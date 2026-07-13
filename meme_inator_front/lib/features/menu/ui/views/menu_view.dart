import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:go_router/go_router.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_states.dart';
import 'package:meme_inator_front/features/auth/ui/pages/login_page.dart';
import 'package:meme_inator_front/features/auth/ui/viewmodels/auth_viewmodel.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/menu/ui/bloc/menu_state.dart';
import 'package:meme_inator_front/features/menu/ui/viewmodels/menu_cubit.dart';
import 'package:meme_inator_front/features/menu/ui/widgets/logout_dialog_widget.dart';
import 'package:meme_inator_front/features/menu/ui/widgets/menu_btn_widget.dart';
import 'package:meme_inator_front/features/menu/ui/widgets/profile_dashboard_widget.dart';
import 'package:meme_inator_front/features/registration/ui/pages/registration_page.dart';
import 'package:meme_inator_front/features/search/ui/pages/search_page.dart';

class MenuView extends StatelessWidget {
  final Function(FeedConfig) onSelectFeed;

  const MenuView({
    required this.onSelectFeed,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return _MenuContent(onSelectFeed: onSelectFeed);
  }
}

class _MenuContent extends StatefulWidget {
  final Function(FeedConfig) onSelectFeed;
  const _MenuContent({required this.onSelectFeed});

  @override
  State<_MenuContent> createState() => _MenuContentState();
}

class _MenuContentState extends State<_MenuContent> {
  late final PageController _pageController;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();

    // After the first frame, jump to the page matching the cubit's selected index
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      final currentIndex = context.read<MenuCubit>().state.selectedIndex;
      if (_pageController.hasClients && _pageController.page != currentIndex) {
        _pageController.jumpToPage(currentIndex);
      }
    });
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isLoggedIn = context.watch<AuthViewModel>().state is Authenticated;

    final scaffoldBg = const Color.fromARGB(236, 245, 245, 245);
    const tabLabelColor = Colors.blue;
    const tabUnselectedColor = Colors.grey;
    const buttonBg = Colors.blue;
    const buttonFg = Colors.white;
    const iconColor = Colors.black87;

    return ColoredBox(
      color: scaffoldBg,
      child: BlocBuilder<MenuCubit, MenuState>(
        builder: (context, state) {
          return Column(
            children: [
              _buildTabBar(context, state.selectedIndex),
              Expanded(
                child: BlocListener<MenuCubit, MenuState>(
                  listenWhen: (prev, curr) =>
                      prev.selectedIndex != curr.selectedIndex,
                  listener: (context, state) async {
                    await _pageController.animateToPage(
                      state.selectedIndex,
                      duration: const Duration(milliseconds: 500),
                      curve: Curves.decelerate,
                    );
                  },
                  child: PageView(
                    controller: _pageController,
                    onPageChanged: (index) {
                      context.read<MenuCubit>().selectTab(index);
                    },
                    children: [
                      _buildMemesTab(
                        context,
                        buttonBg: const Color.fromARGB(255, 238, 115, 34),
                        buttonFg: Colors.white,
                        iconColor: Colors.black87,
                      ),
                      if (isLoggedIn) _buildUserPagesTab(
                              context,
                              buttonBg: Colors.blue,
                              buttonFg: Colors.white,
                              iconColor: Colors.black87,
                            ) else _buildLoginRegisterTab(
                              context,
                              buttonBg: Colors.blue,
                              buttonFg: Colors.white,
                            ),
                    ],
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  // -------------------- Helper Methods --------------------

  Widget _buildTabBar(BuildContext context, int selectedIndex) {
    return PlatformWidget(
      material: (_, __) => TabBar(
        onTap: (index) => context.read<MenuCubit>().selectTab(index),
        labelColor: Colors.blue,
        unselectedLabelColor: Colors.grey,
        indicatorColor: Colors.blue,
        tabs: const [
          Tab(text: 'Memes'),
          Tab(text: 'User Pages'),
        ],
      ),
      cupertino: (_, __) => Padding(
        padding: const EdgeInsets.all(8),
        child: SizedBox(
          width: double.infinity,
          child: CupertinoSegmentedControl<int>(
            groupValue: selectedIndex,
            selectedColor: Colors.blue,
            unselectedColor: Colors.grey,
            borderColor: Colors.grey,
            pressedColor: Colors.blue.withOpacity(0.5),
            children: const {
              0: Padding(
                padding: EdgeInsets.symmetric(horizontal: 16),
                child: Text('Memes'),
              ),
              1: Padding(
                padding: EdgeInsets.symmetric(horizontal: 16),
                child: Text('User Pages'),
              ),
            },
            onValueChanged: (i) => context.read<MenuCubit>().selectTab(i),
          ),
        ),
      ),
    );
  }

  Widget _buildMemesTab(
    BuildContext context, {
    required Color buttonBg,
    required Color buttonFg,
    required Color iconColor,
  }) {
    final headingStyle = Theme.of(context).textTheme.bodyLarge?.copyWith(
      fontWeight: FontWeight.bold,
      color: Colors.black87,
    );

    final onSelectFeed = widget.onSelectFeed;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text('Poppin\' Meme Pages', style: headingStyle),
          MenuButtonWidget(
            text: 'Popular Today',
            onPressed: () => onSelectFeed(FeedConfig.createPopularToday()),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
          MenuButtonWidget(
            text: 'Popular Weekly',
            onPressed: () =>
                onSelectFeed(FeedConfig.createPopularWeekly()),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
          MenuButtonWidget(
            text: 'Popular Monthly',
            onPressed: () =>
                onSelectFeed(FeedConfig.createPopularMonthly()),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
          MenuButtonWidget(
            text: 'Popular Randomized',
            onPressed: () =>
                onSelectFeed(FeedConfig.createRandomizedPopular()),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
          const SizedBox(height: 24),
          Text('Memes pages', style: headingStyle),
          MenuButtonWidget(
            text: 'Recent',
            onPressed: () =>
                onSelectFeed(FeedConfig.createRecent()),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
          MenuButtonWidget(
            text: 'Images',
            onPressed: () =>
                onSelectFeed(FeedConfig.createImagesOnly()),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
          MenuButtonWidget(
            text: 'Videos',
            onPressed: () =>
                onSelectFeed(FeedConfig.createVideosOnly()),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
          const SizedBox(height: 48),
          Row(
            children: [
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildIconButton(
                    context,
                    icon: Icons.search,
                    cupertinoIcon: CupertinoIcons.search,
                    color: iconColor,
                    onPressed: () => showPlatformModalSheet(
                      context: context,
                      builder: (_) => const SearchPage(),
                    ),
                  ),
                  _buildIconButton(
                    context,
                    icon: Icons.settings,
                    cupertinoIcon: CupertinoIcons.settings,
                    color: iconColor,
                    onPressed: () {
                      // TODO: Implement settings
                    },
                  ),
                ],
              ),
              const Spacer(),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildUserPagesTab(
    BuildContext context, {
    required Color buttonBg,
    required Color buttonFg,
    required Color iconColor,
  }) {
    final onSelectFeed = widget.onSelectFeed;
    return ListView(
      physics: const NeverScrollableScrollPhysics(), 
      padding: const EdgeInsets.all(16),
      children: [
        const ProfileDashboardWidget(),
        MenuButtonWidget(
          text: 'My Profile Page',
          onPressed: () async {
            await GoRouter.of(context).push('/profile');
          },
          backgroundColor: buttonBg,
          foregroundColor: buttonFg,
        ),
        MenuButtonWidget(
          text: "My Following's Liked Posts Feed",
          onPressed: () => onSelectFeed(FeedConfig.createFollowingsLiked()),
          backgroundColor: buttonBg,
          foregroundColor: buttonFg,
        ),
        MenuButtonWidget(
          text: "My Friend's Liked Posts Feed",
          onPressed: () => onSelectFeed(FeedConfig.createFriendsLiked()),
          backgroundColor: buttonBg,
          foregroundColor: buttonFg,
        ),
        MenuButtonWidget( 
          text: 'My Liked Memes Feed',
          onPressed: () => onSelectFeed(FeedConfig.createMyLikedMemes()),
          backgroundColor: buttonBg,
          foregroundColor: buttonFg,
        ),
        MenuButtonWidget(
          text: 'My Commented Feed',
          onPressed: () => onSelectFeed(FeedConfig.createCommentedFeeds()),
          backgroundColor: buttonBg,
          foregroundColor: buttonFg,
        ),
        MenuButtonWidget(
          text: 'Workshop',
          onPressed: () => _showComingSoonDialog(context),
          backgroundColor: buttonBg,
          foregroundColor: buttonFg,
        ),
        const SizedBox(height: 48),
        Center(
          child: _buildIconButton(
            context,
            icon: Icons.logout,
            cupertinoIcon: CupertinoIcons.square_arrow_right,
            color: iconColor,
            onPressed: () => const LogoutDialogWidget().show(context),
          ),
        ),
      ],
    );
  }

  Widget _buildLoginRegisterTab(
    BuildContext context, {
    required Color buttonBg,
    required Color buttonFg,
  }) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          _buildActionButton(
            context,
            label: 'Login',
            onPressed: () => showPlatformModalSheet(
              context: context,
              material: MaterialModalSheetData(
                isScrollControlled: true,
              ),
              builder: (_) => const LoginPage(),
            ),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
          const SizedBox(height: 16), 
          _buildActionButton(
            context,
            label: 'Register',
            onPressed: () => showPlatformModalSheet(
              context: context,
              material: MaterialModalSheetData(
                isScrollControlled: true,
              ),
              builder: (_) => const RegisterPage(),
            ),
            backgroundColor: buttonBg,
            foregroundColor: buttonFg,
          ),
        ],
      ),
    );
  }

  // Builds a platform‑adaptive icon button
  Widget _buildIconButton(
    BuildContext context, {
    required IconData icon,
    required IconData cupertinoIcon,
    required Color color,
    required VoidCallback onPressed,
  }) {
    return PlatformIconButton(
      icon: Icon(
        isMaterial(context) ? icon : cupertinoIcon,
        color: color,
      ),
      onPressed: onPressed,
      material: (_, __) => MaterialIconButtonData(
        padding: EdgeInsets.zero,
      ),
      cupertino: (_, __) => CupertinoIconButtonData(
        padding: EdgeInsets.zero,
      ),
    );
  }

  // Builds a platform‑adaptive filled button (used for Login/Register)
  Widget _buildActionButton(
    BuildContext context, {
    required String label,
    required VoidCallback onPressed,
    required Color backgroundColor,
    required Color foregroundColor,
  }) {
    return PlatformElevatedButton(
      child: Text(
        label,
        style: TextStyle(color: foregroundColor),
      ),
      onPressed: onPressed,
      material: (_, __) => MaterialElevatedButtonData(
        style: ElevatedButton.styleFrom(
          backgroundColor: backgroundColor,
        ),
      ),
      cupertino: (_, __) => CupertinoElevatedButtonData(
        color: backgroundColor,
        pressedOpacity: 0.7,
      ),
    );
  }

  void _showComingSoonDialog(BuildContext context) {
    showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: const Text('Coming soon...'),
        actions: [
          PlatformDialogAction(
            child: PlatformText('OK'),
            onPressed: () => GoRouter.of(context).pop(),
          ),
        ],
      ),
    );
  }
}
