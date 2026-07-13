import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';

typedef PlatformPopupMenuItemBuilder<T> = List<PopupMenuItem<T>> Function(BuildContext context);

/// A platform‑adaptive popup menu button.
/// - On Android / Material: uses [PopupMenuButton].
/// - On iOS: uses a [CupertinoButton] that shows a [CupertinoActionSheet].
class PlatformPopupMenuButton<T> extends StatelessWidget {
  final PlatformPopupMenuItemBuilder<T> itemBuilder;
  final void Function(T)? onSelected;
  final bool enabled;
  final Widget child; // typically an icon

  const PlatformPopupMenuButton({
    Key? key,
    required this.itemBuilder,
    this.onSelected,
    this.enabled = true,
    required this.child,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return PlatformWidget(
      material: (_, __) => PopupMenuButton<T>(
        enabled: enabled,
        onSelected: onSelected,
        itemBuilder: (context) => itemBuilder(context),
        child: child,
      ),
      cupertino: (_, __) => CupertinoButton(
        padding: EdgeInsets.zero,
        minSize: 0,
        onPressed: enabled ? () => _showCupertinoMenu(context) : null,
        child: child,
      ),
    );
  }

  void _showCupertinoMenu(BuildContext context) {
    final items = itemBuilder(context);
    if (items.isEmpty) return;
    showCupertinoModalPopup(
      context: context,
      builder: (context) => CupertinoActionSheet(
        actions: items.map((item) {
          return CupertinoActionSheetAction(
            onPressed: () {
              Navigator.pop(context);
              if (onSelected != null && item.value != null) {
                onSelected!(item.value as T);
              }
            },
            child: item.child ?? const SizedBox(),
          );
        }).toList(),
      ),
    );
  }
}