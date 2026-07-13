// lib/core/audio/safe_audio_player.dart
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:just_audio/just_audio.dart';

/// A safe wrapper around [AudioPlayer] that prevents crashes on unsupported platforms.
class SafeAudioPlayer {
  final AudioPlayer _player = AudioPlayer();

  /// Expose the inner player if needed (e.g., for widgets like [AudioSlider]).
  AudioPlayer get rawPlayer => _player;

  /// Initialize and set the audio source.
  Future<void> setSource(Uri uri, {bool loop = false}) async {
    try {
      await _player.setAudioSource(AudioSource.uri(uri));
      if (loop) {
        await _player.setLoopMode(LoopMode.one);
      }
    } catch (e, st) {
      debugPrint('SafeAudioPlayer: Failed to set source: $e\n$st');
    }
  }

  /// Play safely.
  Future<void> play() async {
    try {
      await _player.play();
    } catch (e, st) {
      debugPrint('SafeAudioPlayer: play failed: $e\n$st');
    }
  }

  /// Pause safely.
  Future<void> pause() async {
    try {
      await _player.pause();
    } catch (e, st) {
      debugPrint('SafeAudioPlayer: pause failed: $e\n$st');
    }
  }

  /// Stop safely.
  Future<void> stop() async {
    try {
      await _player.stop();
    } catch (e, st) {
      debugPrint('SafeAudioPlayer: stop failed: $e\n$st');
    }
  }

  /// Dispose safely.
  Future<void> dispose() async {
    try {
      await _player.dispose();
    } catch (e, st) {
      debugPrint('SafeAudioPlayer: dispose failed: $e\n$st');
    }
  }

  /// Set pitch if supported (only on Android/iOS/macOS).
  Future<void> setPitch(double pitch) async {
    if (kIsWeb) {
      debugPrint('SafeAudioPlayer: setPitch not supported on web.');
      return;
    }
    try {
      await _player.setPitch(pitch);
    } on MissingPluginException catch (_) {
      debugPrint('SafeAudioPlayer: setPitch not supported on this platform.');
    } catch (e, st) {
      debugPrint('SafeAudioPlayer: setPitch failed: $e\n$st');
    }
  }
}