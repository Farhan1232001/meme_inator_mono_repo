import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:go_router/go_router.dart';
import 'package:meme_inator_front/features/registration/ui/bloc/registration_states.dart';
import 'package:meme_inator_front/features/registration/ui/viewmodels/registration_viewmodel.dart';
import 'package:meme_inator_front/features/registration/ui/widgets/password_field.dart';

class RegisterView extends StatefulWidget {
  const RegisterView({super.key});

  @override
  State<RegisterView> createState() => _RegisterViewState();
}

class _RegisterViewState extends State<RegisterView> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  bool _acceptTerms = false;


  @override
  void dispose() {
    _emailController.dispose();
    _usernameController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return PlatformScaffold(
      appBar: _buildAppBar(),
      body: BlocListener<RegistrationViewModel, RegistrationState>(
        listener: (context, state) {
          if (state is RegistrationSuccess) {
            _showSuccessDialog(context, state.result.requiresVerification);
          } else if (state is RegistrationError) {
            _showErrorDialog(context, state.message);
          }
        },
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildHeader(),
                const SizedBox(height: 20),
                _buildForm(),
                const SizedBox(height: 8),
                _buildTermsRow(),
                const SizedBox(height: 12),
                _buildRegisterButton(),
                const SizedBox(height: 12),
                _buildOrDivider(),
                const SizedBox(height: 12),
                _buildSocialRow(),
                const SizedBox(height: 8),
                _buildLoginLink(),
                const SizedBox(height: 10),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // -------------------- App Bar --------------------
  PlatformAppBar _buildAppBar() {
    return PlatformAppBar(
      title: const Text('Register'),
      leading: PlatformIconButton(
        icon: Icon(context.platformIcons.back),
        onPressed: () => GoRouter.of(context).pop(),
      ),
    );
  }

  // -------------------- Header Section --------------------
  Column _buildHeader() {
    final theme = Theme.of(context);
    return Column(
      children: [
        const SizedBox(height: 20),
        Center(
          child: PlatformText(
            'Create Account',
            style: theme.textTheme.headlineMedium,
          ),
        ),
        const SizedBox(height: 20),
        Center(
          child: PlatformText(
            'Join the Meme-inator community',
            style: theme.textTheme.bodyMedium,
          ),
        ),
      ],
    );
  }

  // -------------------- Form --------------------
  Widget _buildForm() {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _buildEmailField(),
          const SizedBox(height: 16),
          _buildUsernameField(),
          const SizedBox(height: 16),
          _buildPasswordField(),
          const SizedBox(height: 16),
          _buildConfirmPasswordField(),
        ],
      ),
    );
  }

  Widget _buildEmailField() {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        PlatformText('Email', style: theme.textTheme.titleSmall),
        const SizedBox(height: 8),
        PlatformTextFormField(
          controller: _emailController,
          textInputAction: TextInputAction.next,
          keyboardType: TextInputType.emailAddress,
          hintText: 'Enter your email',
          autofillHints: const [AutofillHints.email],
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
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          ),
          validator: _validateEmail,
        ),
      ],
    );
  }

  String? _validateEmail(String? value) {
    if (value == null || value.trim().isEmpty) return 'Please enter your email';
    if (kDebugMode) return null;
    if (!RegExp(r'^[^@]+@[^@]+\.[^@]+').hasMatch(value))
      return 'Please enter a valid email';
    return null;
  }

  Widget _buildUsernameField() {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        PlatformText('Username', style: theme.textTheme.titleSmall),
        const SizedBox(height: 8),
        PlatformTextFormField(
          controller: _usernameController,
          textInputAction: TextInputAction.next,
          hintText: 'Choose a username',
          autofillHints: const [AutofillHints.username],
          material: (_, __) => MaterialTextFormFieldData(
            decoration: InputDecoration(
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(2),
              ),
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 16,
                vertical: 7,
              ),
            ),
          ),
          cupertino: (_, __) => CupertinoTextFormFieldData(
            decoration: BoxDecoration(
              border: Border.all(color: theme.dividerColor),
              borderRadius: BorderRadius.circular(8),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          ),
          validator: _validateUsername,
        ),
      ],
    );
  }

  String? _validateUsername(String? value) {
    if (value == null || value.trim().isEmpty) return 'Please enter a username';
    if (kDebugMode) return null;
    if (value.length < 3) return 'Username must be at least 3 characters';
    return null;
  }

  Widget _buildPasswordField() {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        PlatformText('Password', style: theme.textTheme.titleSmall),
        const SizedBox(height: 8),
        PlatformPasswordField(
          controller: _passwordController,
          hintText: 'Create a password',
          autofillHints: const [AutofillHints.newPassword],
          textInputAction: TextInputAction.next,
          validator: _validatePassword,
        ),
      ],
    );
  }


  String? _validatePassword(String? value) {
    if (value == null || value.isEmpty) return 'Please enter a password';
    if (kDebugMode) return null;
    if (value.length < 8) return 'Password must be at least 8 characters';
    return null;
  }

  Widget _buildConfirmPasswordField() {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        PlatformText('Confirm Password', style: theme.textTheme.titleSmall),
        const SizedBox(height: 8),
        PlatformPasswordField(
          controller: _confirmPasswordController,
          hintText: 'Re-enter your password',
          autofillHints: const [AutofillHints.newPassword],
          textInputAction: TextInputAction.done,
          validator: _validateConfirmPassword,
          isConfirm: true,
        ),
      ],
    );
  }



  String? _validateConfirmPassword(String? value) {
    if (value == null || value.isEmpty) return 'Please confirm your password';
    if (kDebugMode) return null;
    if (value != _passwordController.text) return 'Passwords do not match';
    return null;
  }

  // -------------------- Terms Row --------------------
  Widget _buildTermsRow() {
    final theme = Theme.of(context);
    return Row(
      children: [
        PlatformCheckbox(
          value: _acceptTerms,
          onChanged: (bool? value) =>
              setState(() => _acceptTerms = value ?? false),
          material: (_, __) =>
              MaterialCheckboxData(visualDensity: VisualDensity.compact),
        ),
        Expanded(
          child: GestureDetector(
            onTap: () => setState(() => _acceptTerms = !_acceptTerms),
            child: PlatformText(
              'I accept the Terms and Conditions',
              style: theme.textTheme.bodyMedium,
            ),
          ),
        ),
      ],
    );
  }

  // -------------------- Register Button --------------------
  Widget _buildRegisterButton() {
    return BlocBuilder<RegistrationViewModel, RegistrationState>(
      builder: (context, state) {
        final isLoading = state is RegistrationLoading;
        return PlatformElevatedButton(
          onPressed: isLoading || !_acceptTerms ? null : _onRegisterPressed,
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
              ? const PlatformCircularProgressIndicator()
              : const Text(
                  'Register',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
        );
      },
    );
  }

  void _onRegisterPressed() {
    if (_formKey.currentState?.validate() ?? false) {
      context.read<RegistrationViewModel>().register(
        email: _emailController.text.trim(),
        username: _usernameController.text.trim(),
        password: _passwordController.text,
      );
    }
  }

  // -------------------- "Or Sign Up with" Divider --------------------
  Widget _buildOrDivider() {
    final theme = Theme.of(context);
    return Row(
      children: [
        const Expanded(child: Divider(thickness: 1)),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: PlatformText(
            'Or Sign Up with',
            style: theme.textTheme.bodyMedium,
          ),
        ),
        const Expanded(child: Divider(thickness: 1)),
      ],
    );
  }

  // -------------------- Social Buttons --------------------
  Widget _buildSocialRow() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _buildSocialButton(
          icon: Icons.g_mobiledata,
          label: 'Google',
          onPressed: () => _showComingSoon(context),
        ),
        const SizedBox(width: 16),
        _buildSocialButton(
          icon: Icons.facebook,
          label: 'Facebook',
          onPressed: () => _showComingSoon(context),
        ),
      ],
    );
  }

  Widget _buildSocialButton({
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
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        ),
      ),
      cupertino: (_, __) => CupertinoElevatedButtonData(
        color: CupertinoColors.systemGrey,
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
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

  // -------------------- Login Link --------------------
  Widget _buildLoginLink() {
    final theme = Theme.of(context);
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        PlatformText(
          'Already have an account? ',
          style: theme.textTheme.bodyMedium,
        ),
        PlatformTextButton(
          onPressed: () => GoRouter.of(context).push('/login'),
          child: Text(
            'Login Now',
            style: TextStyle(
              color: theme.primaryColor,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    );
  }

  // -------------------- Dialogs --------------------
  Future<void> _showSuccessDialog(
    BuildContext context,
    bool requiresVerification,
  ) async {
    await showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: const Text('Registration Successful'),
        content: PlatformText(
          requiresVerification
              ? 'Your account has been created. Please check your email to verify your account before logging in.'
              : 'Your account has been created successfully! You can now log in.',
        ),
        actions: [
          PlatformDialogAction(
            child: const Text('OK'),
            onPressed: () {
              Navigator.pop(context);
              GoRouter.of(context).push('/login');
            },
          ),
        ],
      ),
    );
  }

  Future<void> _showErrorDialog(BuildContext context, String message) async {
    await showPlatformDialog(
      context: context,
      builder: (_) => PlatformAlertDialog(
        title: const Text('Registration Failed'),
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

  void _showComingSoon(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('This feature is coming soon!'),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }
}
