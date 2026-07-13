// lib/core/results.dart
// ignore_for_file: avoid_redundant_argument_values

import 'package:equatable/equatable.dart';

/// Base sealed class for Result pattern
sealed class Result<T> extends Equatable {
  const Result();
  
  /// Pattern matching helper
  R match<R>({
    required R Function(T value) ok,
    required R Function(NotOk<T> notOk) notOk,
    required R Function(Error<T> error) error,
  }) {
    return switch (this) {
      Ok<T>(value: final value) => ok(value),
      NotOk<T>() => notOk(this as NotOk<T>),
      Error<T>() => error(this as Error<T>),
    };
  }

  /// Async pattern matching helper
  Future<R> matchAsync<R>({
    required Future<R> Function(T value) ok,
    required Future<R> Function(NotOk<T> notOk) notOk,
    required Future<R> Function(Error<T> error) error,
  }) async {
    return switch (this) {
      Ok<T>(value: final value) => await ok(value),
      NotOk<T>() => await notOk(this as NotOk<T>),
      Error<T>() => await error(this as Error<T>),
    };
  }
  
  /// Safe value accessor
  T? get valueOrNull => match<T?>(
    ok: (value) => value,
    notOk: (_) => null,
    error: (_) => null,
  );
  
  /// Check if result is Ok
  bool get isOk => this is Ok<T>;
  
  /// Check if result is NotOk
  bool get isNotOk => this is NotOk<T>;
  
  /// Check if result is Error
  bool get isError => this is Error<T>;
}

/// Success result with value
class Ok<T> extends Result<T> {
  final T value;
  
  const Ok(this.value);
  
  @override
  List<Object?> get props => [value];
  
  @override
  String toString() => 'Ok(value: $value)';
}

/// Business logic failure (expected errors)
class NotOk<T> extends Result<T> {
  final String message;
  final String? staticMessage;
  final int statusCode;
  
  const NotOk({
    required this.message,
    this.staticMessage,
    this.statusCode = 400,
  });
  
  factory NotOk.badRequest({String? message, String? staticMessage}) => NotOk(
    message: message ?? 'Bad Request',
    staticMessage: staticMessage,
    statusCode: 400,
  );
  
  factory NotOk.unauthorized({String? message, String? staticMessage}) => NotOk(
    message: message ?? 'Unauthorized',
    staticMessage: staticMessage,
    statusCode: 401,
  );
  
  factory NotOk.forbidden({String? message, String? staticMessage}) => NotOk(
    message: message ?? 'Forbidden',
    staticMessage: staticMessage,
    statusCode: 403,
  );
  
  factory NotOk.notFound({String? message, String? staticMessage}) => NotOk(
    message: message ?? 'Not Found',
    staticMessage: staticMessage,
    statusCode: 404,
  );
  
  factory NotOk.conflict({String? message, String? staticMessage}) => NotOk(
    message: message ?? 'Conflict',
    staticMessage: staticMessage,
    statusCode: 409,
  );
  
  factory NotOk.validationError({String? message, String? staticMessage}) => NotOk(
    message: message ?? 'Validation Error',
    staticMessage: staticMessage,
    statusCode: 422,
  );
  
  @override
  List<Object?> get props => [message, staticMessage, statusCode];
  
  @override
  String toString() => 'NotOk(message: $message, staticMessage: $staticMessage, statusCode: $statusCode)';
}

/// Unexpected/technical failure (exceptions)
class Error<T> extends Result<T> {
  final String message;
  final String? staticMessage;
  final Exception? exception;
  final int statusCode;
  final StackTrace? stackTrace;
  
  const Error({
    this.message = 'Internal Server Error',
    this.staticMessage = 'SERVER_ERROR',
    this.exception,
    this.statusCode = 500,
    this.stackTrace,
  });
  
  factory Error.fromException(
    Exception exception, {
    String? message,
    String? staticMessage,
    int? statusCode,
    StackTrace? stackTrace,
  }) => Error(
    message: message ?? exception.toString(),
    staticMessage: staticMessage ?? 'EXCEPTION_OCCURRED',
    exception: exception,
    statusCode: statusCode ?? 500,
    stackTrace: stackTrace ?? StackTrace.current,
  );
  
  factory Error.networkError({
    String? message,
    String? staticMessage,
    Exception? exception,
    StackTrace? stackTrace,
  }) => Error(
    message: message ?? 'Network Error',
    staticMessage: staticMessage ?? 'NETWORK_ERROR',
    exception: exception,
    statusCode: 503,
    stackTrace: stackTrace,
  );
  
  factory Error.timeout({
    String? message,
    String? staticMessage,
    Exception? exception,
    StackTrace? stackTrace,
  }) => Error(
    message: message ?? 'Request Timeout',
    staticMessage: staticMessage ?? 'TIMEOUT_ERROR',
    exception: exception,
    statusCode: 408,
    stackTrace: stackTrace,
  );
  
  @override
  List<Object?> get props => [message, staticMessage, exception, statusCode, stackTrace];
  
  @override
  String toString() => 'Error(message: $message, staticMessage: $staticMessage, '
      'exception: $exception, statusCode: $statusCode)';
}