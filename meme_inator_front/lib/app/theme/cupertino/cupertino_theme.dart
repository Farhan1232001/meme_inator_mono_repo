// lib/theme/cupertino/cupertino_theme.dart

import 'package:flutter/cupertino.dart';
import '../app_colors.dart';

class CupertinoAppTheme {
  static CupertinoThemeData get lightTheme {
    return const CupertinoThemeData(
      brightness: Brightness.light,
      primaryColor: AppColors.cupertinoAccentColor,
      scaffoldBackgroundColor: CupertinoColors.systemGroupedBackground,
      barBackgroundColor: CupertinoColors.systemBackground,
      textTheme: CupertinoTextThemeData(
        textStyle: TextStyle(fontSize: 16, color: CupertinoColors.label),
        actionTextStyle: TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.bold,
          color: AppColors.cupertinoAccentColor,
        ),
        navTitleTextStyle:
            TextStyle(fontSize: 20, fontWeight: FontWeight.w600),
        navLargeTitleTextStyle:
            TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
        tabLabelTextStyle:
            TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
      ),
    );
  }

  static CupertinoThemeData get darkTheme {
    return const CupertinoThemeData(
      brightness: Brightness.dark,
      primaryColor: AppColors.cupertinoAccentColor,
      scaffoldBackgroundColor: CupertinoColors.systemGroupedBackground,
      barBackgroundColor: CupertinoColors.systemBackground,
      textTheme: CupertinoTextThemeData(
        textStyle: TextStyle(fontSize: 16, color: CupertinoColors.label),
        actionTextStyle: TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.bold,
          color: AppColors.cupertinoAccentColor,
        ),
        navTitleTextStyle: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: CupertinoColors.label,
        ),
        navLargeTitleTextStyle: TextStyle(
          fontSize: 28,
          fontWeight: FontWeight.bold,
          color: CupertinoColors.label,
        ),
        tabLabelTextStyle: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w500,
          color: CupertinoColors.label,
        ),
      ),
    );
  }

  // Convenience getters for platform-aware segmented control
  static Color get segmentedSelectedColor => AppColors.cupertinoAccentColor;
  static Color get segmentedUnselectedColor => CupertinoColors.systemGrey5;
  static Color get segmentedBorderColor => AppColors.cupertinoAccentColor;
  static Color get segmentedPressedColor =>
      AppColors.cupertinoAccentColor.withOpacity(0.12);
}