import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:go_router/go_router.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_events.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_states.dart';
import 'package:meme_inator_front/features/auth/ui/viewmodels/auth_viewmodel.dart';
// features/auth/ui/views/login_view.dart
// ... (keep all imports the same)

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _rememberMe = false;

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return PlatformScaffold(
      appBar: _buildAppBar(),
      body: BlocConsumer<AuthViewModel, AuthState>(
        listener: _authListener,
        builder: (context, state) {
          // Show loading overlay if needed
          final isLoading = state is AuthLoadingState;

          return Stack(
            children: [
              SafeArea(
                child: SingleChildScrollView(
                  physics: const NeverScrollableScrollPhysics(),
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const SizedBox(height: 40),
                      _buildTitleSection(),
                      const SizedBox(height: 40),
                      _buildForm(),
                      const SizedBox(height: 16),
                      _buildRememberMeRow(),
                      const SizedBox(height: 24),
                      _buildLoginButton(),
                      const SizedBox(height: 24),
                      _buildOrDivider(),
                      const SizedBox(height: 24),
                      _buildSocialButtons(),
                      const SizedBox(height: 10),
                      _buildSignUpRow(),
                      const SizedBox(height: 10),
                    ],
                  ),
                ),
              ),
              if (isLoading)
                const ColoredBox(
                  color: Colors.black54,
                  child: Center(
                    child: PlatformCircularProgressIndicator(),
                  ),
                ),
            ],
          );
        },
      ),
    );
  }

  // AppBar
  PlatformAppBar _buildAppBar() {
    return PlatformAppBar(
      title: const Text('Login'),
      leading: PlatformIconButton(
        icon: Icon(context.platformIcons.back),
        onPressed: () => GoRouter.of(context).pop(),
      ),
    );
  }

  // Title Section
  Widget _buildTitleSection() {
    final theme = Theme.of(context);
    return Center(
      child: PlatformText(
        'Meme-inator',
        style: theme.textTheme.displayLarge,
      ),
    );
  }

  // Login Form
  Widget _buildForm() {
    final theme = Theme.of(context);
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Username/Email Field
          PlatformText(
            'Username or Email',
            style: theme.textTheme.titleSmall,
          ),
          const SizedBox(height: 8),
          PlatformTextFormField(
            controller: _usernameController,
            textInputAction: TextInputAction.next,
            keyboardType: TextInputType.emailAddress,
            hintText: 'Enter your username or email',
            autofillHints: const [AutofillHints.username],
            material: (_, __) => MaterialTextFormFieldData(
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 14,
                ),
              ),
            ),
            cupertino: (_, __) => CupertinoTextFormFieldData(
              decoration: BoxDecoration(
                border: Border.all(color: theme.dividerColor),
                borderRadius: BorderRadius.circular(8),
              ),
              padding: const EdgeInsets.symmetric(
                horizontal: 16,
                vertical: 14,
              ),
            ),
            validator: (value) {
              if (value == null || value.trim().isEmpty) {
                return 'Please enter your username or email';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),

          // Password Field
          PlatformText(
            'Password',
            style: theme.textTheme.titleSmall,
          ),
          const SizedBox(height: 8),
          PlatformTextFormField(
            controller: _passwordController,
            textInputAction: TextInputAction.done,
            obscureText: true,
            hintText: 'Enter your password',
            autofillHints: const [AutofillHints.password],
            material: (_, __) => MaterialTextFormFieldData(
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 14,
                ),
              ),
            ),
            cupertino: (_, __) => CupertinoTextFormFieldData(
              decoration: BoxDecoration(
                border: Border.all(color: theme.dividerColor),
                borderRadius: BorderRadius.circular(8),
              ),
              padding: const EdgeInsets.symmetric(
                horizontal: 16,
                vertical: 14,
              ),
            ),
            validator: (value) {
              if (value == null || value.trim().isEmpty) {
                return 'Please enter your password';
              }
              if (kDebugMode) return null;
              if (value.length < 6) {
                return 'Password must be at least 6 characters';
              }
              return null;
            },
          ),
        ],
      ),
    );
  }

  // Remember Me & Forgot Password Row
  Widget _buildRememberMeRow() {
    final theme = Theme.of(context);
    return Row(
      children: [
        PlatformCheckbox(
          value: _rememberMe,
          onChanged: (bool? value) {
            setState(() {
              _rememberMe = value ?? false;
            });
          },
          material: (_, __) => MaterialCheckboxData(
            visualDensity: VisualDensity.compact,
          ),
        ),
        PlatformText(
          'Remember Me',
          style: theme.textTheme.bodyMedium,
        ),
        const Spacer(),
        PlatformTextButton(
          onPressed: () => GoRouter.of(context).push('/forgot-password'),
          child: const Text(
            'Forgot Password?',
            style: TextStyle(
              color: Colors.grey,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ],
    );
  }

  // Login Button (with loading state)
  Widget _buildLoginButton() {
    return BlocBuilder<AuthViewModel, AuthState>(
      builder: (context, state) {
        final isLoading = state is AuthLoadingState;
        return PlatformElevatedButton(
          onPressed: isLoading
              ? null
              : () {
                  if (_formKey.currentState?.validate() ?? false) {
                    context.read<AuthViewModel>().add(
                      AuthLoginRequestedEvent(
                        username: _usernameController.text.trim(),
                        password: _passwordController.text,
                        rememberMe: _rememberMe,
                      ),
                    );
                  }
                },
          material: (_, __) => MaterialElevatedButtonData(
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ),
          cupertino: (_, __) => CupertinoElevatedButtonData(
            padding: const EdgeInsets.symmetric(vertical: 16),
          ),
          child: isLoading
              ? const SizedBox(
                  height: 20,
                  width: 20,
                  child: PlatformCircularProgressIndicator(),
                )
              : const Text(
                  'Log In',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
        );
      },
    );
  }

  // "Or Sign In with" Divider
  Widget _buildOrDivider() {
    final theme = Theme.of(context);
    return Row(
      children: [
        const Expanded(child: Divider(thickness: 1)),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: PlatformText(
            'Or Sign In with',
            style: theme.textTheme.bodyMedium,
          ),
        ),
        const Expanded(child: Divider(thickness: 1)),
      ],
    );
  }

  // Social Login Buttons Row
  Widget _buildSocialButtons() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _buildSocialLoginButton(
          icon: Icons.g_mobiledata,
          label: 'Google',
          onPressed: () => _showComingSoon(context),
        ),
        const SizedBox(width: 16),
        _buildSocialLoginButton(
          icon: Icons.facebook,
          label: 'Facebook',
          onPressed: () => _showComingSoon(context),
        ),
      ],
    );
  }

  // Sign Up Link Row
  Widget _buildSignUpRow() {
    final theme = Theme.of(context);
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        PlatformText(
          "Don't have an account? ",
          style: theme.textTheme.bodyMedium,
        ),
        PlatformTextButton(
          onPressed: () => GoRouter.of(context).push('/register'),
          child: Text(
            'Register Now',
            style: TextStyle(
              color: theme.primaryColor,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    );
  }

  // Helper for social login buttons
  Widget _buildSocialLoginButton({
    required IconData icon,
    required String label,
    required VoidCallback onPressed,
  }) {
    return PlatformElevatedButton(
      onPressed: onPressed,
      material: (_, __) => MaterialElevatedButtonData(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.grey[200],
          foregroundColor: Colors.black87,
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 12,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      cupertino: (_, __) => CupertinoElevatedButtonData(
        color: CupertinoColors.systemGrey,
        padding: const EdgeInsets.symmetric(
          horizontal: 24,
          vertical: 12,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 20),
          const SizedBox(width: 8),
          Text(label),
        ],
      ),
    );
  }

  // BLoC listener logic
  void _authListener(BuildContext context, AuthState state) {
    if (state is Authenticated) {
      // Check if we're in a modal sheet
      final navigator = Navigator.of(context);

      // Close the modal sheet if we're in one
      if (navigator.canPop()) {
        navigator.pop();
      }

      // Navigate to home
      GoRouter.of(context).go('/home');
    } else if (state is AuthErrorState) {
      _showErrorDialog(context, state.message);
    } else if (state is UnauthenticatedState && state.clearMessage != null) {
      _showInfoSnackBar(context, state.clearMessage!);
    }
  }

  void _showErrorDialog(BuildContext context, String message) {
    showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: const Text('Login Failed'),
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

  void _showInfoSnackBar(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        behavior: SnackBarBehavior.floating,
        backgroundColor: Theme.of(context).primaryColor,
      ),
    );
  }

  void _showComingSoon(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('This feature is coming soon!'),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }
}
