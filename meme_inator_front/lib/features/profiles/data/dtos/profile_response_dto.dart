import 'package:json_annotation/json_annotation.dart';

part 'profile_response_dto.g.dart';

@JsonSerializable()
class ProfileResponseDto {
  @JsonKey(name: 'user_id')
  final String userId;
  
  @JsonKey(name: 'username')
  final String username;
  
  @JsonKey(name: 'description')
  final String? description;
  
  @JsonKey(name: 'background_color')
  final String? backgroundColor;
  
  @JsonKey(name: 'profile_pic_url')
  final String? profilePicUrl;
  
  @JsonKey(name: 'profile_header_img_url')
  final String? profileHeaderImgUrl;
  
  @JsonKey(name: 'bg_img')
  final String? bgImg;
  
  @JsonKey(name: 'profile_theme_music_url')
  final String? profileThemeMusicUrl;
  
  @JsonKey(name: 'is_online_msg')
  final String? isOnlineMsg;
  
  @JsonKey(name: 'is_offline_msg')
  final String? isOfflineMsg;
  
  @JsonKey(name: 'upload_count')
  final int uploadCount;
  
  @JsonKey(name: 'followers_count')
  final int followersCount;
  
  @JsonKey(name: 'following_count')
  final int followingCount;
  
  @JsonKey(name: 'friends_count')
  final int friendsCount;
  
  @JsonKey(name: 'likes_given')
  final int likesGiven;
  
  @JsonKey(name: 'posts_uploaded')
  final int postsUploaded;
  
  @JsonKey(name: 'comments_posted')
  final int commentsPosted;
  
  @JsonKey(name: 'dislikes_given')
  final int dislikesGiven;
  
  @JsonKey(name: 'last_updated')
  final String lastUpdated;

  /// Relationship Related attributes (Fellowship/friendships)
  @JsonKey(name: 'is_following')
  final bool? isFollowing;

  ProfileResponseDto({
    required this.userId,
    required this.username,
    this.description,
    this.backgroundColor,
    this.profilePicUrl,
    this.profileHeaderImgUrl,
    this.bgImg,
    required this.profileThemeMusicUrl,
    this.isOnlineMsg,
    this.isOfflineMsg,
    required this.uploadCount,
    required this.followersCount,
    required this.followingCount,
    required this.friendsCount,
    required this.likesGiven,
    required this.postsUploaded,
    required this.commentsPosted,
    required this.dislikesGiven,
    required this.lastUpdated,
    this.isFollowing = false
  });

  factory ProfileResponseDto.fromJson(Map<String, dynamic> json) =>
      _$ProfileResponseDtoFromJson(json);
      
  Map<String, dynamic> toJson() => _$ProfileResponseDtoToJson(this);
}