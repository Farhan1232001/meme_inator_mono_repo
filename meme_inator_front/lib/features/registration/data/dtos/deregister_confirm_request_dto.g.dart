// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'deregister_confirm_request_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

DeregisterConfirmRequestDto _$DeregisterConfirmRequestDtoFromJson(
  Map<String, dynamic> json,
) => DeregisterConfirmRequestDto(
  token: json['token'] as String,
  challengeCode: json['challenge_code'] as String?,
);

Map<String, dynamic> _$DeregisterConfirmRequestDtoToJson(
  DeregisterConfirmRequestDto instance,
) => <String, dynamic>{
  'token': instance.token,
  'challenge_code': instance.challengeCode,
};
