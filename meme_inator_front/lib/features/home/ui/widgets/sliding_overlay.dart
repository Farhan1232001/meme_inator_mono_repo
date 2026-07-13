import 'package:flutter/material.dart';

class SlidingOverlay extends StatelessWidget {
  final Widget base;
  final Widget overlay;
  final bool showOverlay;
  final Duration duration;
  final Duration reverseDuration;
  final Curve switchInCurve;
  final Curve switchOutCurve;
  final Offset slideBeginOffset;

  const SlidingOverlay({
    super.key,
    required this.base,
    required this.overlay,
    required this.showOverlay,
    this.duration = const Duration(milliseconds: 900),
    this.reverseDuration = const Duration(milliseconds: 500),
    this.switchInCurve = Curves.bounceOut,
    this.switchOutCurve = Curves.easeIn,
    this.slideBeginOffset = const Offset(-1.5, 0),
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        base,
        AnimatedSwitcher(
          duration: duration,
          reverseDuration: reverseDuration,
          switchInCurve: switchInCurve,
          switchOutCurve: switchOutCurve,
          transitionBuilder: (child, animation) => SlideTransition(
            position: Tween<Offset>(
              begin: slideBeginOffset,
              end: Offset.zero,
            ).animate(animation),
            child: child,
          ),
          child: showOverlay ? overlay : const SizedBox.shrink(),
        ),
      ],
    );
  }
}