import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/registration/domain/repositories/iregistration_repo.dart';
import 'package:meme_inator_front/features/registration/ui/bloc/registration_states.dart';

class RegistrationViewModel extends Cubit<RegistrationState> {
  final IRegistrationRepository _repository;

  RegistrationViewModel({required IRegistrationRepository repository, required authRepository})
      : _repository = repository,
        super(const RegistrationInitial());

  Future<void> register({
    required String email,
    required String username,
    required String password,
  }) async {
    emit(const RegistrationLoading());
    final result = await _repository.register(
      email: email,
      username: username,
      rawPassword: password,
    );
    result.match(
      ok: (regResult) => emit(RegistrationSuccess(result: regResult)),
      notOk: (notOk) => emit(RegistrationError(message: notOk.message)),
      error: (error) => emit(RegistrationError(message: error.message)),
    );
  }

  Future<void> verifyRegistration({required String token}) async {
    emit(const RegistrationLoading());
    final result = await _repository.verifyRegistration(token: token);
    result.match(
      ok: (verifyResult) => emit(RegistrationVerifySuccess(result: verifyResult)),
      notOk: (notOk) => emit(RegistrationError(message: notOk.message)),
      error: (error) => emit(RegistrationError(message: error.message)),
    );
  }

  Future<void> deregister({
    required String refreshToken,
    required String password,
  }) async {
    emit(const RegistrationLoading());
    final result = await _repository.deregister(
      refreshToken: refreshToken,
      rawPassword: password,
    );
    result.match(
      ok: (_) => emit(const DeregisterInitiated()),
      notOk: (notOk) => emit(RegistrationError(message: notOk.message)),
      error: (error) => emit(RegistrationError(message: error.message)),
    );
  }

  Future<void> confirmDeregistration({
    required String token,
    String? challengeCode,
  }) async {
    emit(const RegistrationLoading());
    final result = await _repository.confirmDeregistration(
      token: token,
      challengeCode: challengeCode,
    );
    result.match(
      ok: (confirmResult) => emit(DeregisterConfirmSuccess(result: confirmResult)),
      notOk: (notOk) => emit(RegistrationError(message: notOk.message)),
      error: (error) => emit(RegistrationError(message: error.message)),
    );
  }

  void reset() {
    emit(const RegistrationInitial());
  }
}