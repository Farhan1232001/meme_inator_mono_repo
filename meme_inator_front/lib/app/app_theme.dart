// lib/app_theme.dart

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:meme_inator_front/app/theme/cupertino/cupertino_theme.dart';
import 'package:meme_inator_front/app/theme/material/material_theme.dart';

export 'theme/app_colors.dart';
export 'theme/material/material_theme.dart';
export 'theme/material/material_theme_extensions.dart';
export 'theme/cupertino/cupertino_theme.dart';
export 'theme/cupertino/cupertino_theme_extensions.dart';

/// Main AppTheme class that provides the theme configurations
class AppTheme {
  // Material themes
  static ThemeData get materialLightTheme => MaterialTheme.lightTheme;
  static ThemeData get materialDarkTheme => MaterialTheme.darkTheme;

  // Cupertino themes
  static CupertinoThemeData get cupertinoLightTheme =>
      CupertinoAppTheme.lightTheme;
  static CupertinoThemeData get cupertinoDarkTheme =>
      CupertinoAppTheme.darkTheme;

  // Platform-aware theme getters
  static ThemeData materialOf(BuildContext context) {
    final isDark = MediaQuery.of(context).platformBrightness == Brightness.dark;
    return isDark ? materialDarkTheme : materialLightTheme;
  }

  static CupertinoThemeData cupertinoOf(BuildContext context) {
    final isDark = MediaQuery.of(context).platformBrightness == Brightness.dark;
    return isDark ? cupertinoDarkTheme : cupertinoLightTheme;
  }

  // Helper to determine which theme to use
  static bool isMaterial(BuildContext context) {
    // You can implement your own logic here based on platform or preference
    // For example, check platform or use a setting
    return true; // Default to Material
  }

  // Convenience method to get appropriate theme based on platform
  static dynamic themeOf(BuildContext context) {
    return isMaterial(context) ? materialOf(context) : cupertinoOf(context);
  }
}