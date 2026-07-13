import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
// import 'package:meme_inator0/l10n/l10n.dart';
import 'package:meme_inator_front/l10n/gen/app_localizations.dart';

extension PumpApp on WidgetTester {
  Future<void> pumpApp(Widget widget) {
    return pumpWidget(
      MaterialApp(
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: widget,
      ),
    );
  }
}
