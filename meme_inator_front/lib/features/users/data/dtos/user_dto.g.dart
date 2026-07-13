// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

UserDto _$UserDtoFromJson(Map<String, dynamic> json) => UserDto(
  id: uuidFromJson(json['id'] as String),
  username: json['username'] as String,
  email: json['email'] as String,
  isOnline: json['is_online'] as bool? ?? false,
  isProUser: json['is_pro_user'] as bool? ?? false,
  isVerified: json['is_verified'] as bool? ?? false,
  isBanned: json['is_banned'] as bool? ?? false,
  dateJoined: json['date_joined'] == null
      ? null
      : DateTime.parse(json['date_joined'] as String),
  profile: json['profile'] == null
      ? null
      : ProfileEntity.fromJson(json['profile'] as Map<String, dynamic>),
  isSoftDeleted: json['is_soft_deleted'] as bool? ?? false,
);

Map<String, dynamic> _$UserDtoToJson(UserDto instance) => <String, dynamic>{
  'id': uuidToJson(instance.id),
  'username': instance.username,
  'email': instance.email,
  'is_online': instance.isOnline,
  'is_pro_user': instance.isProUser,
  'is_verified': instance.isVerified,
  'is_banned': instance.isBanned,
  'date_joined': instance.dateJoined.toIso8601String(),
  'profile': instance.profile?.toJson(),
  'is_soft_deleted': instance.isSoftDeleted,
};
