// ignore_for_file: cascade_invocations

import 'package:bloc/bloc.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/auth/domain/repositories/iauth_repo.dart';
import 'package:meme_inator_front/features/auth/domain/usecases/get_current_user_from_token_usecase.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_events.dart';
import 'package:meme_inator_front/features/auth/ui/bloc/auth_states.dart';
import 'package:uuid/uuid_value.dart';

// TODO: GET rid of repository, use the usecases!!! my guy.
class AuthViewModel extends Bloc<AuthEvent, AuthState> {
  final IAuthRepository _authRepository;
  late final GetCurrentUserFromTokenUsecase _getCurrentUserFromToken;

  late String? _currentUserId;
  String? get currentUserId => _currentUserId;

  AuthViewModel({required IAuthRepository authRepository})
    : _authRepository = authRepository,
      super(const AuthInitialState()) {
    on<AuthLoginRequestedEvent>(_onLoginRequested);
    on<AuthLogoutRequestedEvent>(_onLogoutRequested);
    on<AuthCheckStatusRequestedEvent>(_onCheckStatus);
    on<AuthRefreshTokenRequestedEvent>(_onRefreshToken);

    _getCurrentUserFromToken = GetCurrentUserFromTokenUsecase(_authRepository);
  }

  // In AuthViewModel._onLoginRequested
  Future<void> _onLoginRequested(
    AuthLoginRequestedEvent event,
    Emitter<AuthState> emit,
  ) async {
    emit(const AuthLoadingState());

    try {
      final result = await _authRepository
          .login(
            usernameOrEmail: event.username,
            password: event.password,
            rememberMe: event.rememberMe,
          )
          .timeout(const Duration(seconds: 30));

      await result.match(
        ok: (tokenPair) async {
          // 1. store _currentUserId
          final currentUserResult = await _getCurrentUserFromToken.execute(tokenPair);
          if (currentUserResult is Ok) {
            _currentUserId = currentUserResult.valueOrNull;
          }
          
          emit(Authenticated(tokenPair: tokenPair));
        },
        notOk: (notOk) async => emit(AuthErrorState(message: notOk.message)),
        error: (error)async  => emit(AuthErrorState(message: error.message)),
      );
    } catch (e) {
      emit(AuthErrorState(message: 'Login timeout or network error: $e'));
    }
  }

  Future<void> _onLogoutRequested(
    AuthLogoutRequestedEvent event,
    Emitter<AuthState> emit,
  ) async {
    emit(const AuthLoadingState());
    final result = await _authRepository.logout();
    result.match(
      ok: (_) {
        _currentUserId = null;
         emit(const UnauthenticatedState());
      },
      notOk: (notOk) => emit(AuthErrorState(message: notOk.message)),
      error: (error) => emit(AuthErrorState(message: error.message)),
    );
  }

  Future<void> _onCheckStatus(
    AuthCheckStatusRequestedEvent event,
    Emitter<AuthState> emit,
  ) async {
    // Don't emit loading if we already have a valid state
    if (state is! Authenticated) {
      emit(const AuthLoadingState());
    }
    final result = await _authRepository.isLoggedIn();
    result.match(
      ok: (isLoggedIn) {
        if (isLoggedIn) {
          // Optionally fetch token pair to pass to Authenticated state
          _authRepository.getStoredTokenPair().then((tokenResult) {
            tokenResult.match(
              ok: (pair) {
                if (pair != null) {
                  emit(Authenticated(tokenPair: pair));
                } else {
                  emit(const UnauthenticatedState());
                }
              },
              notOk: (_) => emit(const UnauthenticatedState()),
              error: (_) => emit(const UnauthenticatedState()),
            );
          });
        } else {
          emit(const UnauthenticatedState());
        }
      },
      notOk: (_) => emit(const UnauthenticatedState()),
      error: (_) => emit(const UnauthenticatedState()),
    );
  }

  Future<void> _onRefreshToken(
    AuthRefreshTokenRequestedEvent event,
    Emitter<AuthState> emit,
  ) async {
    final currentState = state;
    if (currentState is Authenticated) {
      emit(const AuthLoadingState());
      final result = await _authRepository.refreshToken(
        refreshToken: currentState.tokenPair.refreshToken,
      );
      result.match(
        ok: (newPair) => emit(Authenticated(tokenPair: newPair)),
        notOk: (notOk) async {
          // Refresh failed, force logout
          await _authRepository.clearTokenPair();
          emit(UnauthenticatedState(clearMessage: notOk.message));
        },
        error: (error) async {
          await _authRepository.clearTokenPair();
          emit(UnauthenticatedState(clearMessage: error.message));
        },
      );
    }
  }

  Future<String?> getCurrentUserFromToken() async {
    final result = await _getCurrentUserFromToken.execute(null);

    return result.match(
      ok: (userId) => userId,
      notOk: (_) => null,
      error: (_) => null,
    );
  }
}
