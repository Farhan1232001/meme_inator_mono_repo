// lib/core/observers/bloc_observer.dart
// ignore_for_file: cascade_invocations

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:logging/logging.dart';

class AppBlocObserver extends BlocObserver {
  final _logger = Logger('AppBlocObserver');
  

  @override
  void onCreate(BlocBase bloc) {
    super.onCreate(bloc);
    _logger.info('╔══════════════════════════════════════════════╗');
    _logger.info('║ 🎯 BLOC CREATED                              ║');
    _logger.info('╠══════════════════════════════════════════════╣');
    _logger.info('║ Type: ${bloc.runtimeType}');
    if (bloc.state != null) {
      _logger.info('║ Initial State: ${_formatState(bloc.state)}');
    }
    _logger.info('╚══════════════════════════════════════════════╝');
  }

  @override
  void onEvent(Bloc bloc, Object? event) {
    super.onEvent(bloc, event);
    _logger.info('╔══════════════════════════════════════════════╗');
    _logger.info('║ 📨 EVENT FIRED                               ║');
    _logger.info('╠══════════════════════════════════════════════╣');
    _logger.info('║ Bloc: ${bloc.runtimeType}');
    _logger.info('║ Event: ${_formatState(event)}');
    _logger.info('╚══════════════════════════════════════════════╝');
  }

  @override
  void onTransition(Bloc bloc, Transition transition) {
    super.onTransition(bloc, transition);
    _logger.info('╔══════════════════════════════════════════════╗');
    _logger.info('║ 🔄 TRANSITION                                ║');
    _logger.info('╠══════════════════════════════════════════════╣');
    _logger.info('║ Bloc: ${bloc.runtimeType}');
    _logger.info('║ Event: ${_formatState(transition.event)}');
    _logger.info('║ From: ${_formatState(transition.currentState)}');
    _logger.info('║ To: ${_formatState(transition.nextState)}');
    _logger.info('╚══════════════════════════════════════════════╝');
  }

  @override
  void onChange(BlocBase bloc, Change change) {
    super.onChange(bloc, change);
    _logger.fine('╔══════════════════════════════════════════════╗');
    _logger.fine('║ 📊 STATE CHANGE                              ║');
    _logger.fine('╠══════════════════════════════════════════════╣');
    _logger.fine('║ Bloc: ${bloc.runtimeType}');
    _logger.fine('║ Current: ${_formatState(change.currentState)}');
    _logger.fine('║ Next: ${_formatState(change.nextState)}');
    _logger.fine('╚══════════════════════════════════════════════╝');
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    _logger.severe('╔══════════════════════════════════════════════╗');
    _logger.severe('║ ❌ ERROR OCCURRED                            ║');
    _logger.severe('╠══════════════════════════════════════════════╣');
    _logger.severe('║ Bloc: ${bloc.runtimeType}                    ║');
    _logger.severe('║ Error: $error                                ║');
    _logger.severe('║ StackTrace: $stackTrace                      ║');
    _logger.severe('╚══════════════════════════════════════════════╝');
    super.onError(bloc, error, stackTrace);
  }

  @override
  void onClose(BlocBase bloc) {
    super.onClose(bloc);
    _logger.info('╔══════════════════════════════════════════════╗');
    _logger.info('║ 🔚 BLOC CLOSED                               ║');
    _logger.info('╠══════════════════════════════════════════════╣');
    _logger.info('║ Type: ${bloc.runtimeType}');
    _logger.info('╚══════════════════════════════════════════════╝');
  }

  // Helper method to format state objects nicely
  String _formatState(Object? state) {
    if (state == null) return 'null';
    
    // Try to get a readable representation
    try {
      final string = state.toString();
      // Truncate very long strings
      if (string.length > 200) {
        return '${string.substring(0, 200)}...';
      }
      return string;
    } catch (e) {
      return state.runtimeType.toString();
    }
  }

}