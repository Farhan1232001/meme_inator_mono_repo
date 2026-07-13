
import 'package:json_annotation/json_annotation.dart';
import 'package:meme_inator_front/core/utils/uuid_utils.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:uuid/uuid.dart';

part 'user_dto.g.dart';


@JsonSerializable(explicitToJson: true)
class UserDto {
  @JsonKey(fromJson: uuidFromJson, toJson: uuidToJson)
  final UuidValue id;

  final String username;
  final String email;

  @JsonKey(name: 'is_online')
  final bool isOnline;

  @JsonKey(name: 'is_pro_user')
  final bool isProUser;

  @JsonKey(name: 'is_verified')
  final bool isVerified;

  @JsonKey(name: 'is_banned')
  final bool isBanned;

  @JsonKey(name: 'date_joined')
  final DateTime dateJoined;

  final ProfileEntity? profile;

  @JsonKey(name: 'is_soft_deleted')
  final bool isSoftDeleted;

  UserDto({
    required this.id,
    required this.username,
    required this.email,
    this.isOnline = false,
    this.isProUser = false,
    this.isVerified = false,
    this.isBanned = false,
    DateTime? dateJoined,
    this.profile,
    this.isSoftDeleted = false,
  }) : dateJoined = dateJoined ?? DateTime.now().toUtc();

  factory UserDto.fromJson(Map<String, dynamic> json) => _$UserDtoFromJson(json);
  Map<String, dynamic> toJson() => _$UserDtoToJson(this);

}
