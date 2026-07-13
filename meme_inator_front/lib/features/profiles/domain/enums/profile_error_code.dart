// lib/domain/enums/profile_error_code.dart

/// Enhanced enum to mirror the Python `ProfileErrorCode` string values.
enum ProfileErrorCode {
  PROFILE_NOT_FOUND('PROFILE_NOT_FOUND');

  final String value;
  const ProfileErrorCode(this.value);

  @override
  String toString() => value;

  /// Construct from a string value (case-sensitive).
  factory ProfileErrorCode.fromString(String s) {
    return ProfileErrorCode.values.firstWhere(
      (e) => e.value == s,
      orElse: () => throw ArgumentError('Unknown ProfileErrorCode: $s'),
    );
  }
}
