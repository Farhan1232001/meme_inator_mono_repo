// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'registration_request_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

RegistrationRequestDto _$RegistrationRequestDtoFromJson(
  Map<String, dynamic> json,
) => RegistrationRequestDto(
  email: json['email'] as String,
  username: json['username'] as String,
  rawPassword: json['raw_password'] as String,
);

Map<String, dynamic> _$RegistrationRequestDtoToJson(
  RegistrationRequestDto instance,
) => <String, dynamic>{
  'email': instance.email,
  'username': instance.username,
  'raw_password': instance.rawPassword,
};
