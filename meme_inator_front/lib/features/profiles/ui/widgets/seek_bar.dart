// lib/widgets/audio_slider.dart
import 'dart:math';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:just_audio/just_audio.dart';
import 'package:meme_inator_front/core/audio/safe_audio_player.dart';
import 'package:rxdart/rxdart.dart';

/// Data class for audio position information.
class PositionData {
  final Duration position;
  final Duration bufferedPosition;
  final Duration duration;

  PositionData(this.position, this.bufferedPosition, this.duration);
}

/// Reusable slider with play/pause button and time display.
/// Based on the prototype’s SeekBar.
class SeekBar extends StatefulWidget {
  final Duration duration;
  final Duration position;
  final Duration bufferedPosition;
  final bool isPlaying;
  final VoidCallback onPlayPauseToggle;
  final ValueChanged<Duration>? onChanged;
  final ValueChanged<Duration>? onChangeEnd;

  const SeekBar({
    Key? key,
    required this.duration,
    required this.position,
    required this.bufferedPosition,
    required this.isPlaying,
    required this.onPlayPauseToggle,
    this.onChanged,
    this.onChangeEnd,
  }) : super(key: key);

  @override
  SeekBarState createState() => SeekBarState();
}

class SeekBarState extends State<SeekBar> {
  double? _dragValue;

  @override
  Widget build(BuildContext context) {
    final maxMs = widget.duration.inMilliseconds.toDouble();
    final positionMs = widget.position.inMilliseconds.toDouble();
    final dragMs = _dragValue ?? positionMs;

    return Row(
      children: [
        _buildPlayPauseButton(),
        Expanded(
          child: PlatformSlider(
            min: 0.0,
            max: maxMs > 0 ? maxMs : 1.0,
            value: min(dragMs, maxMs),
            onChanged: (value) {
              setState(() => _dragValue = value);
              widget.onChanged?.call(Duration(milliseconds: value.round()));
            },
            onChangeEnd: (value) {
              widget.onChangeEnd?.call(Duration(milliseconds: value.round()));
              setState(() => _dragValue = null);
            },
            material: (_, __) => MaterialSliderData(
              thumbColor: Colors.transparent,
              activeColor: Colors.blue,
            ),
            cupertino: (_, __) => CupertinoSliderData(
              thumbColor: Colors.transparent,
            ),
          ),
        ),
        const SizedBox(width: 8),
        Text(
          _formatDuration(widget.duration - widget.position),
          style: _platformTextStyle(context),
        ),
      ],
    );
  }

  Widget _buildPlayPauseButton() {
    return PlatformWidget(
      material: (_, __) => IconButton(
        icon: Icon(widget.isPlaying ? Icons.pause : Icons.play_arrow, size: 20),
        onPressed: widget.onPlayPauseToggle,
        padding: EdgeInsets.zero,
        constraints: BoxConstraints.tight(Size(32, 32)),
        visualDensity: VisualDensity.compact,
      ),
      cupertino: (_, __) => CupertinoButton(
        padding: EdgeInsets.zero,
        minimumSize: const Size(32, 32),
        onPressed: widget.onPlayPauseToggle,
        child: Icon(
          widget.isPlaying ? CupertinoIcons.pause : CupertinoIcons.play,
          size: 20,
          color: CupertinoColors.activeBlue,
        ),
      ),
    );
  }

  TextStyle _platformTextStyle(BuildContext context) {
    return isCupertino(context)
        ? CupertinoTheme.of(context).textTheme.textStyle.copyWith(fontSize: 12)
        : Theme.of(context).textTheme.bodySmall ?? const TextStyle(fontSize: 12);
  }
}

String _formatDuration(Duration d) {
  String twoDigits(int n) => n.toString().padLeft(2, '0');
  final minutes = twoDigits(d.inMinutes.remainder(60));
  final seconds = twoDigits(d.inSeconds.remainder(60));
  final hours = d.inHours;
  return hours > 0 ? '$hours:$minutes:$seconds' : '$minutes:$seconds';
}

/// A ready‑to‑use audio widget that displays a slider and play/pause.
/// It takes an [AudioPlayer] instance (typically from a [SafeAudioPlayer]).
class AudioSlider extends StatefulWidget {
  final AudioPlayer player;

  const AudioSlider({Key? key, required this.player}) : super(key: key);

  @override
  State<AudioSlider> createState() => _AudioSliderState();
}

class _AudioSliderState extends State<AudioSlider> {
  Stream<PositionData> get _positionDataStream =>
      Rx.combineLatest3<Duration, Duration, Duration?, PositionData>(
        widget.player.positionStream,
        widget.player.bufferedPositionStream,
        widget.player.durationStream,
        (position, bufferedPosition, duration) => PositionData(
          position,
          bufferedPosition,
          duration ?? Duration.zero,
        ),
      );

  Future<void> _togglePlayPause() async {
    if (widget.player.playing) {
      await widget.player.pause();
    } else {
      await widget.player.play();
    }
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<PositionData>(
      stream: _positionDataStream,
      builder: (context, snapshot) {
        final data = snapshot.data ??
            PositionData(Duration.zero, Duration.zero, Duration.zero);
        return SeekBar(
          duration: data.duration,
          position: data.position,
          bufferedPosition: data.bufferedPosition,
          onChangeEnd: widget.player.seek,
          isPlaying: widget.player.playing,
          onPlayPauseToggle: _togglePlayPause,
        );
      },
    );
  }
}