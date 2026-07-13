import 'dart:io' show Platform;
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';

class PlatformPasswordField extends StatefulWidget {
  final TextEditingController controller;
  final String hintText;
  final String? label;
  final String? Function(String?)? validator;
  final Iterable<String>? autofillHints;
  final TextInputAction? textInputAction;
  final void Function(String)? onFieldSubmitted;
  final bool isConfirm; // optional flag if you want slightly different UI/semantics

  const PlatformPasswordField({
    Key? key,
    required this.controller,
    this.hintText = '',
    this.label,
    this.validator,
    this.autofillHints,
    this.textInputAction,
    this.onFieldSubmitted,
    this.isConfirm = false,
  }) : super(key: key);

  @override
  _PlatformPasswordFieldState createState() => _PlatformPasswordFieldState();
}

class _PlatformPasswordFieldState extends State<PlatformPasswordField> {
  bool _obscure = true;

  void _toggle() => setState(() => _obscure = !_obscure);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    // Build a PlatformTextFormField that handles Material suffix and
    // provides extra right padding for Cupertino so we can overlay an icon.
    final field = PlatformTextFormField(
      controller: widget.controller,
      obscureText: _obscure,
      textInputAction: widget.textInputAction,
      autofillHints: widget.autofillHints?.toList(),
      onFieldSubmitted: widget.onFieldSubmitted,
      validator: widget.validator,
      material: (_, __) => MaterialTextFormFieldData(
        decoration: InputDecoration(
          hintText: widget.hintText,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          // Material supports suffixIcon natively:
          suffixIcon: IconButton(
            icon: Icon(
              _obscure ? Icons.visibility_off : Icons.visibility,
              size: 20,
            ),
            onPressed: _toggle,
            splashRadius: 20,
            padding: const EdgeInsets.all(8),
            constraints: const BoxConstraints(minWidth: 40, minHeight: 40),
          ),
        ),
      ),
      cupertino: (_, __) => CupertinoTextFormFieldData(
        placeholder: widget.hintText,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14)
            .copyWith(right: 48), // extra right padding for the overlay icon
        decoration: BoxDecoration(
          border: Border.all(color: theme.dividerColor),
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );

    // On iOS we overlay a Cupertino style button on top-right of the textfield.
    if (Platform.isIOS) {
      return Stack(
        alignment: Alignment.centerRight,
        children: [
          field,
          // Positioned to match textfield internal padding
          Positioned(
            right: 6,
            child: Padding(
              padding: const EdgeInsets.only(right: 6.0),
              child: CupertinoButton(
                minSize: 30,
                padding: const EdgeInsets.all(6),
                child: Icon(
                  _obscure ? CupertinoIcons.eye_slash : CupertinoIcons.eye,
                  size: 20,
                ),
                onPressed: _toggle,
              ),
            ),
          ),
        ],
      );
    } else {
      // Material / default: just return the PlatformTextFormField (it contains suffixIcon)
      return field;
    }
  }
}