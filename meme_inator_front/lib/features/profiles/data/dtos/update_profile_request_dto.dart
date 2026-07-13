import 'package:json_annotation/json_annotation.dart';

part 'update_profile_request_dto.g.dart';

@JsonSerializable(includeIfNull: false)
class UpdateProfileRequestDto {
  final String? description;
  final String? backgroundColor;
  final String? profilePicUrl;
  final String? profileHeaderImgUrl;
  final String? bgImg;
  final String? profileThemeMusicUrl;
  final String? isOnlineMsg;
  final String? isOfflineMsg;

  UpdateProfileRequestDto({
    this.description,
    this.backgroundColor,
    this.profilePicUrl,
    this.profileHeaderImgUrl,
    this.bgImg,
    this.profileThemeMusicUrl,
    this.isOnlineMsg,
    this.isOfflineMsg,
  });

  factory UpdateProfileRequestDto.fromJson(Map<String, dynamic> json) =>
      _$UpdateProfileRequestDtoFromJson(json);
  Map<String, dynamic> toJson() => _$UpdateProfileRequestDtoToJson(this);
}