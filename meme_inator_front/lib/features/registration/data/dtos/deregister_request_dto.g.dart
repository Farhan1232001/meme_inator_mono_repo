// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'deregister_request_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

DeregisterRequestDto _$DeregisterRequestDtoFromJson(
  Map<String, dynamic> json,
) => DeregisterRequestDto(
  refreshToken: json['refresh_token'] as String,
  rawPassword: json['raw_password'] as String,
);

Map<String, dynamic> _$DeregisterRequestDtoToJson(
  DeregisterRequestDto instance,
) => <String, dynamic>{
  'refresh_token': instance.refreshToken,
  'raw_password': instance.rawPassword,
};
