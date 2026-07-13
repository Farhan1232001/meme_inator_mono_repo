// lib/theme/material/material_theme_extensions.dart

import 'package:flutter/material.dart';

extension MaterialThemeExtensions on BuildContext {
  // Theme getters
  ThemeData get materialTheme => Theme.of(this);
  bool get isDarkMode => Theme.of(this).brightness == Brightness.dark;

  // Color getters
  Color get appBarBackground => Theme.of(this).appBarTheme.backgroundColor ??
      Theme.of(this).colorScheme.primary;

  Color get appBarForeground => Theme.of(this).appBarTheme.foregroundColor ??
      Theme.of(this).colorScheme.onPrimary;

  Color get dividerColor => Theme.of(this).dividerColor;

  Color get avatarBackground =>
      isDarkMode ? Colors.black26 : Colors.white70;

  Color get textOnBackground =>
      Theme.of(this).textTheme.bodyLarge?.color ??
      Theme.of(this).colorScheme.onSurface;

  Color get scaffoldBackground => Theme.of(this).scaffoldBackgroundColor;

  Color get primaryColor => Theme.of(this).colorScheme.primary;

  Color get onPrimaryColor => Theme.of(this).colorScheme.onPrimary;

  Color get iconColor => Theme.of(this).iconTheme.color ??
      Theme.of(this).colorScheme.onSurface;

  Color get unselectedLabelColor =>
      Theme.of(this).textTheme.bodyMedium?.color ??
      Theme.of(this).colorScheme.onSurface;

  Color get buttonBackground => Theme.of(this).colorScheme.primary;

  Color get buttonForeground => Theme.of(this).colorScheme.onPrimary;

  // Text style getters
  TextStyle get bodyTextStyle => Theme.of(this).textTheme.bodyMedium!;

  TextStyle get usernameTextStyle {
    final base = bodyLargeTextStyle ?? const TextStyle();
    return base.copyWith(
      fontSize: 20,
      fontWeight: FontWeight.bold,
      color: textOnBackground,
    );
  }

  TextStyle get statNumberTextStyle {
    final base = bodyLargeTextStyle ?? const TextStyle();
    return base.copyWith(
      fontSize: 18,
      fontWeight: FontWeight.bold,
      color: textOnBackground,
    );
  }

  TextStyle get statLabelTextStyle {
    final base = bodyTextStyle;
    final color = Theme.of(this).textTheme.bodyMedium?.color?.withOpacity(0.85);
    return base.copyWith(fontSize: 14, color: color);
  }

  TextStyle get appBarTitleTextStyle {
    final base = Theme.of(this).textTheme.titleMedium ?? const TextStyle();
    final color = Theme.of(this).colorScheme.onSurface;

    return TextStyle(
      inherit: false,
      fontSize: base.fontSize ?? 17.0,
      fontWeight: base.fontWeight ?? FontWeight.w600,
      letterSpacing: base.letterSpacing ?? 0.0,
      height: base.height,
      fontFamily: base.fontFamily,
      color: color,
    );
  }

  TextStyle? get bodyLargeTextStyle => Theme.of(this).textTheme.bodyLarge;
}