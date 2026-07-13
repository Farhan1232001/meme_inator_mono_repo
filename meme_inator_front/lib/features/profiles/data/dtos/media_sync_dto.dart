import 'package:json_annotation/json_annotation.dart';

part 'media_sync_dto.g.dart';

@JsonSerializable()
class MediaSyncDto {
  final String? profilePictureKey;
  final String? headerImageKey;
  final String? backgroundImageKey;
  final String? themeMusicKey;

  MediaSyncDto({
    this.profilePictureKey,
    this.headerImageKey,
    this.backgroundImageKey,
    this.themeMusicKey,
  });

  factory MediaSyncDto.fromJson(Map<String, dynamic> json) =>
      _$MediaSyncDtoFromJson(json);
  Map<String, dynamic> toJson() => _$MediaSyncDtoToJson(this);
}