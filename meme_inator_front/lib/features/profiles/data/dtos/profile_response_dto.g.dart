// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'profile_response_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ProfileResponseDto _$ProfileResponseDtoFromJson(Map<String, dynamic> json) =>
    ProfileResponseDto(
      userId: json['user_id'] as String,
      username: json['username'] as String,
      description: json['description'] as String?,
      backgroundColor: json['background_color'] as String?,
      profilePicUrl: json['profile_pic_url'] as String?,
      profileHeaderImgUrl: json['profile_header_img_url'] as String?,
      bgImg: json['bg_img'] as String?,
      profileThemeMusicUrl: json['profile_theme_music_url'] as String?,
      isOnlineMsg: json['is_online_msg'] as String?,
      isOfflineMsg: json['is_offline_msg'] as String?,
      uploadCount: (json['upload_count'] as num).toInt(),
      followersCount: (json['followers_count'] as num).toInt(),
      followingCount: (json['following_count'] as num).toInt(),
      friendsCount: (json['friends_count'] as num).toInt(),
      likesGiven: (json['likes_given'] as num).toInt(),
      postsUploaded: (json['posts_uploaded'] as num).toInt(),
      commentsPosted: (json['comments_posted'] as num).toInt(),
      dislikesGiven: (json['dislikes_given'] as num).toInt(),
      lastUpdated: json['last_updated'] as String,
      isFollowing: json['is_following'] as bool? ?? false,
    );

Map<String, dynamic> _$ProfileResponseDtoToJson(ProfileResponseDto instance) =>
    <String, dynamic>{
      'user_id': instance.userId,
      'username': instance.username,
      'description': instance.description,
      'background_color': instance.backgroundColor,
      'profile_pic_url': instance.profilePicUrl,
      'profile_header_img_url': instance.profileHeaderImgUrl,
      'bg_img': instance.bgImg,
      'profile_theme_music_url': instance.profileThemeMusicUrl,
      'is_online_msg': instance.isOnlineMsg,
      'is_offline_msg': instance.isOfflineMsg,
      'upload_count': instance.uploadCount,
      'followers_count': instance.followersCount,
      'following_count': instance.followingCount,
      'friends_count': instance.friendsCount,
      'likes_given': instance.likesGiven,
      'posts_uploaded': instance.postsUploaded,
      'comments_posted': instance.commentsPosted,
      'dislikes_given': instance.dislikesGiven,
      'last_updated': instance.lastUpdated,
      'is_following': instance.isFollowing,
    };
