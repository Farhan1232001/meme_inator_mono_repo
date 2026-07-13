// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'update_profile_request_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

UpdateProfileRequestDto _$UpdateProfileRequestDtoFromJson(
  Map<String, dynamic> json,
) => UpdateProfileRequestDto(
  description: json['description'] as String?,
  backgroundColor: json['backgroundColor'] as String?,
  profilePicUrl: json['profilePicUrl'] as String?,
  profileHeaderImgUrl: json['profileHeaderImgUrl'] as String?,
  bgImg: json['bgImg'] as String?,
  profileThemeMusicUrl: json['profileThemeMusicUrl'] as String?,
  isOnlineMsg: json['isOnlineMsg'] as String?,
  isOfflineMsg: json['isOfflineMsg'] as String?,
);

Map<String, dynamic> _$UpdateProfileRequestDtoToJson(
  UpdateProfileRequestDto instance,
) => <String, dynamic>{
  'description': ?instance.description,
  'backgroundColor': ?instance.backgroundColor,
  'profilePicUrl': ?instance.profilePicUrl,
  'profileHeaderImgUrl': ?instance.profileHeaderImgUrl,
  'bgImg': ?instance.bgImg,
  'profileThemeMusicUrl': ?instance.profileThemeMusicUrl,
  'isOnlineMsg': ?instance.isOnlineMsg,
  'isOfflineMsg': ?instance.isOfflineMsg,
};
