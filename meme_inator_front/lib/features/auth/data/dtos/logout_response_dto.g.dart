// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'logout_response_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

LogoutResponseDto _$LogoutResponseDtoFromJson(Map<String, dynamic> json) =>
    LogoutResponseDto(
      statusCode: (json['status_code'] as num).toInt(),
      staticMsg: json['static_msg'] as String,
      message: json['message'] as String,
    );

Map<String, dynamic> _$LogoutResponseDtoToJson(LogoutResponseDto instance) =>
    <String, dynamic>{
      'status_code': instance.statusCode,
      'static_msg': instance.staticMsg,
      'message': instance.message,
    };
