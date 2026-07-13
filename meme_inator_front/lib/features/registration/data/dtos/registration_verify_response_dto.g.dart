// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'registration_verify_response_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

RegistrationVerifyResponseDto _$RegistrationVerifyResponseDtoFromJson(
  Map<String, dynamic> json,
) => RegistrationVerifyResponseDto(
  verified: json['verified'] as bool,
  userId: json['user_id'] as String,
  message: json['message'] as String,
);

Map<String, dynamic> _$RegistrationVerifyResponseDtoToJson(
  RegistrationVerifyResponseDto instance,
) => <String, dynamic>{
  'verified': instance.verified,
  'user_id': instance.userId,
  'message': instance.message,
};
