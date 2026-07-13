import 'package:meme_inator_front/features/profiles/data/dtos/profile_response_dto.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';

class ProfilesMapper {
  /// Convert map to ProfileEntity
  static ProfileEntity mapToEntity(Map<String, dynamic> map) {
    return ProfileEntity(
      userId: map['user_id'] as String? ?? map['userId'] as String? ?? '',
      username: map['username'] as String? ?? map['username'] as String? ?? '',
      description: map['description'] as String?,
      backgroundColor:
          map['background_color'] as String? ??
          map['backgroundColor'] as String?,
      profilePicUrl:
          map['profile_pic_url'] as String? ?? map['profilePicUrl'] as String?,
      profileHeaderImgUrl:
          map['profile_header_img_url'] as String? ??
          map['profileHeaderImgUrl'] as String?,
      bgImg: map['bg_img'] as String? ?? map['bgImg'] as String?,
      profileThemeMusicUrl:
          map['profile_theme_music_url'] as String? ??
          map['profileThemeMusicUrl'] as String?,
      isOnlineMsg:
          map['is_online_msg'] as String? ?? map['isOnlineMsg'] as String?,
      isOfflineMsg:
          map['is_offline_msg'] as String? ?? map['isOfflineMsg'] as String?,
      uploadCount:
          (map['upload_count'] as int?) ?? (map['uploadCount'] as int?) ?? 0,
      followersCount:
          (map['followers_count'] as int?) ??
          (map['followersCount'] as int?) ??
          0,
      followingCount:
          (map['following_count'] as int?) ??
          (map['followingCount'] as int?) ??
          0,
      friendsCount:
          (map['friends_count'] as int?) ?? (map['friendsCount'] as int?) ?? 0,
      likesGiven:
          (map['likes_given'] as int?) ?? (map['likesGiven'] as int?) ?? 0,
      postsUploaded:
          (map['posts_uploaded'] as int?) ??
          (map['postsUploaded'] as int?) ??
          0,
      commentsPosted:
          (map['comments_posted'] as int?) ??
          (map['commentsPosted'] as int?) ??
          0,
      dislikesGiven:
          (map['dislikes_given'] as int?) ??
          (map['dislikesGiven'] as int?) ??
          0,
      lastUpdated: map['last_updated'] != null
          ? DateTime.parse(map['last_updated'].toString())
          : DateTime.now(),
      isFollowing: map['is_following'] as bool?
    );
  }

  /// Convert ProfileEntity to map
  static Map<String, dynamic> entityToMap(ProfileEntity entity) {
    return {
      'user_id': entity.userId,
      'description': entity.description,
      'background_color': entity.backgroundColor,
      'profile_pic_url': entity.profilePicUrl,
      'profile_header_img_url': entity.profileHeaderImgUrl,
      'bg_img': entity.bgImg,
      'profile_theme_music_url': entity.profileThemeMusicUrl,
      'is_online_msg': entity.isOnlineMsg,
      'is_offline_msg': entity.isOfflineMsg,
      'upload_count': entity.uploadCount,
      'followers_count': entity.followersCount,
      'following_count': entity.followingCount,
      'friends_count': entity.friendsCount,
      'likes_given': entity.likesGiven,
      'posts_uploaded': entity.postsUploaded,
      'comments_posted': entity.commentsPosted,
      'dislikes_given': entity.dislikesGiven,
      'last_updated': entity.lastUpdated.toIso8601String(),
      'is_following': entity.isFollowing
    };
  }

  /// Convert ProfileEntity to JSON (for API)
  static Map<String, dynamic> entityToJson(ProfileEntity entity) {
    return {
      'userId': entity.userId,
      'description': entity.description,
      'backgroundColor': entity.backgroundColor,
      'profilePicUrl': entity.profilePicUrl,
      'profileHeaderImgUrl': entity.profileHeaderImgUrl,
      'bgImg': entity.bgImg,
      'profileThemeMusicUrl': entity.profileThemeMusicUrl,
      'isOnlineMsg': entity.isOnlineMsg,
      'isOfflineMsg': entity.isOfflineMsg,
      'uploadCount': entity.uploadCount,
      'followersCount': entity.followersCount,
      'followingCount': entity.followingCount,
      'friendsCount': entity.friendsCount,
      'likesGiven': entity.likesGiven,
      'postsUploaded': entity.postsUploaded,
      'commentsPosted': entity.commentsPosted,
      'dislikesGiven': entity.dislikesGiven,
      'lastUpdated': entity.lastUpdated.toIso8601String(),
      'is_following': entity.isFollowing
    };
  }

  /// Convert JSON to ProfileEntity (from API)
  static ProfileEntity jsonToEntity(Map<String, dynamic> json) {
    return ProfileEntity(
      userId: json['userId'] as String,
      username: json['username'] as String,
      description: json['description'] as String?,
      backgroundColor: json['backgroundColor'] as String?,
      profilePicUrl: json['profilePicUrl'] as String?,
      profileHeaderImgUrl: json['profileHeaderImgUrl'] as String?,
      bgImg: json['bgImg'] as String?,
      profileThemeMusicUrl: json['profileThemeMusicUrl'] as String?,
      isOnlineMsg: json['isOnlineMsg'] as String?,
      isOfflineMsg: json['isOfflineMsg'] as String?,
      uploadCount: (json['uploadCount'] as num?)?.toInt() ?? 0,
      followersCount: (json['followersCount'] as num?)?.toInt() ?? 0,
      followingCount: (json['followingCount'] as num?)?.toInt() ?? 0,
      friendsCount: (json['friendsCount'] as num?)?.toInt() ?? 0,
      likesGiven: (json['likesGiven'] as num?)?.toInt() ?? 0,
      postsUploaded: (json['postsUploaded'] as num?)?.toInt() ?? 0,
      commentsPosted: (json['commentsPosted'] as num?)?.toInt() ?? 0,
      dislikesGiven: (json['dislikesGiven'] as num?)?.toInt() ?? 0,
      lastUpdated: DateTime.parse(json['lastUpdated'] as String),
      isFollowing: json['is_following'] as bool?
    );
  }

  /// Create a minimal ProfileEntity from user ID
  static ProfileEntity createMinimalProfile(String userId, String username) {
    return ProfileEntity(
      userId: userId,
      username: username,
      lastUpdated: DateTime.now(),
      // All other fields will use their default values
    );
  }

  /// Merge partial data into existing ProfileEntity
  static ProfileEntity mergeWithPartial(
    ProfileEntity existing,
    Map<String, dynamic> partialData,
  ) {
    return ProfileEntity(
      userId: existing.userId,
      username: existing.username,
      description:
          partialData['description'] as String? ?? existing.description,
      backgroundColor:
          partialData['backgroundColor'] as String? ?? existing.backgroundColor,
      profilePicUrl:
          partialData['profilePicUrl'] as String? ?? existing.profilePicUrl,
      profileHeaderImgUrl:
          partialData['profileHeaderImgUrl'] as String? ??
          existing.profileHeaderImgUrl,
      bgImg: partialData['bgImg'] as String? ?? existing.bgImg,
      profileThemeMusicUrl:
          partialData['profileThemeMusicUrl'] as String? ??
          existing.profileThemeMusicUrl,
      isOnlineMsg:
          partialData['isOnlineMsg'] as String? ?? existing.isOnlineMsg,
      isOfflineMsg:
          partialData['isOfflineMsg'] as String? ?? existing.isOfflineMsg,
      uploadCount: (partialData['uploadCount'] as int?) ?? existing.uploadCount,
      followersCount:
          (partialData['followersCount'] as int?) ?? existing.followersCount,
      followingCount:
          (partialData['followingCount'] as int?) ?? existing.followingCount,
      friendsCount:
          (partialData['friendsCount'] as int?) ?? existing.friendsCount,
      likesGiven: (partialData['likesGiven'] as int?) ?? existing.likesGiven,
      postsUploaded:
          (partialData['postsUploaded'] as int?) ?? existing.postsUploaded,
      commentsPosted:
          (partialData['commentsPosted'] as int?) ?? existing.commentsPosted,
      dislikesGiven:
          (partialData['dislikesGiven'] as int?) ?? existing.dislikesGiven,
      lastUpdated: DateTime.now(),
      isFollowing: partialData['is_following'] as bool?
    );
  }

  static ProfileEntity dtoToEntity(ProfileResponseDto dto) {
    return ProfileEntity(
      userId: dto.userId,
      username: dto.username,
      description: dto.description,
      backgroundColor: dto.backgroundColor,
      profilePicUrl: dto.profilePicUrl,
      profileHeaderImgUrl: dto.profileHeaderImgUrl,
      bgImg: dto.bgImg,
      profileThemeMusicUrl: dto.profileThemeMusicUrl,
      isOnlineMsg: dto.isOnlineMsg,
      isOfflineMsg: dto.isOfflineMsg,
      uploadCount: dto.uploadCount,
      followersCount: dto.followersCount,
      followingCount: dto.followingCount,
      friendsCount: dto.friendsCount,
      likesGiven: dto.likesGiven,
      postsUploaded: dto.postsUploaded,
      commentsPosted: dto.commentsPosted,
      dislikesGiven: dto.dislikesGiven,
      lastUpdated: DateTime.parse(dto.lastUpdated),
      isFollowing: dto.isFollowing
    );
  }
}
