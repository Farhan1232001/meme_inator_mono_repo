// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'deregister_confirm_response_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

DeregisterConfirmResponseDto _$DeregisterConfirmResponseDtoFromJson(
  Map<String, dynamic> json,
) => DeregisterConfirmResponseDto(
  success: json['success'] as bool,
  message: json['message'] as String,
);

Map<String, dynamic> _$DeregisterConfirmResponseDtoToJson(
  DeregisterConfirmResponseDto instance,
) => <String, dynamic>{
  'success': instance.success,
  'message': instance.message,
};
