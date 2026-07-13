// lib/theme/cupertino/cupertino_theme_extensions.dart

import 'package:flutter/cupertino.dart';
import '../app_colors.dart';

extension CupertinoThemeExtensions on BuildContext {
  // Theme getters
  CupertinoThemeData get cupertinoTheme => CupertinoTheme.of(this);
  bool get isDarkMode => CupertinoTheme.of(this).brightness == Brightness.dark;

  // Color getters
  Color get appBarBackground =>
      CupertinoTheme.of(this).barBackgroundColor ??
      CupertinoColors.systemBackground;

  Color get appBarForeground =>
      CupertinoTheme.of(this).textTheme.actionTextStyle?.color ??
      CupertinoColors.label;

  Color get dividerColor => CupertinoColors.separator;

  Color get avatarBackground => isDarkMode ? CupertinoColors.black : CupertinoColors.white;

  Color get textOnBackground =>
      CupertinoTheme.of(this).textTheme.textStyle.color ??
      CupertinoColors.label;

  Color get scaffoldBackground =>
      CupertinoTheme.of(this).scaffoldBackgroundColor;

  Color get primaryColor => CupertinoTheme.of(this).primaryColor;

  Color get onPrimaryColor =>
      CupertinoTheme.of(this).textTheme.actionTextStyle?.color ??
      CupertinoColors.white;

  Color get iconColor =>
      CupertinoTheme.of(this).textTheme.textStyle.color ??
      CupertinoColors.label;

  Color get unselectedLabelColor =>
      CupertinoTheme.of(this).textTheme.textStyle.color ??
      CupertinoColors.label;

  Color get buttonBackground => isDarkMode
      ? AppColors.primary.withOpacity(0.85)
      : AppColors.primary;

  Color get buttonForeground => CupertinoColors.white;

  // Text style getters
  TextStyle get bodyTextStyle => CupertinoTheme.of(this).textTheme.textStyle;

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
    final color = CupertinoColors.inactiveGray;
    return base.copyWith(fontSize: 14, color: color);
  }

  TextStyle get appBarTitleTextStyle {
    final base =
        CupertinoTheme.of(this).textTheme.navTitleTextStyle;
    final color =
        CupertinoTheme.of(this).textTheme.navTitleTextStyle.color ??
            CupertinoColors.label;

    return TextStyle(
      inherit: false,
      fontSize: base.fontSize ?? 17.0,
      fontWeight: base.fontWeight ?? FontWeight.w600,
      letterSpacing: base.letterSpacing ?? -0.41,
      height: base.height,
      fontFamily: base.fontFamily,
      color: color,
    );
  }

  TextStyle? get bodyLargeTextStyle =>
      CupertinoTheme.of(this).textTheme.textStyle;
}