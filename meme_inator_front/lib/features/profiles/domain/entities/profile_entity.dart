// lib/domain/entities/profile_entity.dart

/// Domain entity representing a user profile.
/// UUIDs are represented as String here; replace with a Uuid type if you prefer.
class ProfileEntity {
  // --- Identity ---
  final String userId;
  final String username;

  // --- Profile appearance ---
  final String? description;
  final String? backgroundColor;
  final String? profilePicUrl;
  final String? profileHeaderImgUrl;
  final String? bgImg;
  final String? profileThemeMusicUrl;

  // --- Presence messages ---
  final String? isOnlineMsg;
  final String? isOfflineMsg;

  // --- Counters ---
  final int uploadCount;
  final int followersCount;
  final int followingCount;
  final int friendsCount;
  final int likesGiven;
  final int postsUploaded;
  final int commentsPosted;
  final int dislikesGiven;

  // --- Timestamps ---
  final DateTime lastUpdated;

  // --- Followship context ---
  final bool? isFollowing;

  const ProfileEntity({
    required this.userId,
    required this.username,
    this.description,
    this.backgroundColor,
    this.profilePicUrl,
    this.profileHeaderImgUrl,
    this.bgImg,
    this.profileThemeMusicUrl,
    this.isOnlineMsg,
    this.isOfflineMsg,
    this.uploadCount = -1,
    this.followersCount = -1,
    this.followingCount = -1,
    this.friendsCount = -1,
    this.likesGiven = -1,
    this.postsUploaded = -1,
    this.commentsPosted = -1,
    this.dislikesGiven = -1,
    required this.lastUpdated,
    this.isFollowing = null
  });

  ProfileEntity copyWith({
    String? userId,
    String? username,
    String? description,
    String? backgroundColor,
    String? profilePicUrl,
    String? profileHeaderImgUrl,
    String? bgImg,
    String? profileThemeMusicUrl,
    String? isOnlineMsg,
    String? isOfflineMsg,
    int? uploadCount,
    int? followersCount,
    int? followingCount,
    int? friendsCount,
    int? likesGiven,
    int? postsUploaded,
    int? commentsPosted,
    int? dislikesGiven,
    DateTime? lastUpdated,
    bool? isFollowing
  }) {
    return ProfileEntity(
      userId: userId ?? this.userId,
      username: username ?? this.username,
      description: description ?? this.description,
      backgroundColor: backgroundColor ?? this.backgroundColor,
      profilePicUrl: profilePicUrl ?? this.profilePicUrl,
      profileHeaderImgUrl: profileHeaderImgUrl ?? this.profileHeaderImgUrl,
      bgImg: bgImg ?? this.bgImg,
      profileThemeMusicUrl: profileThemeMusicUrl ?? this.profileThemeMusicUrl,
      isOnlineMsg: isOnlineMsg ?? this.isOnlineMsg,
      isOfflineMsg: isOfflineMsg ?? this.isOfflineMsg,
      uploadCount: uploadCount ?? this.uploadCount,
      followersCount: followersCount ?? this.followersCount,
      followingCount: followingCount ?? this.followingCount,
      friendsCount: friendsCount ?? this.friendsCount,
      likesGiven: likesGiven ?? this.likesGiven,
      postsUploaded: postsUploaded ?? this.postsUploaded,
      commentsPosted: commentsPosted ?? this.commentsPosted,
      dislikesGiven: dislikesGiven ?? this.dislikesGiven,
      lastUpdated: lastUpdated ?? this.lastUpdated,
      isFollowing: isFollowing ?? this.isFollowing,
    );
  }

  Map<String, dynamic> toJson() => {
        'userId': userId,
        'username': username,
        'description': description,
        'backgroundColor': backgroundColor,
        'profilePicUrl': profilePicUrl,
        'profileHeaderImgUrl': profileHeaderImgUrl,
        'bgImg': bgImg,
        'profileThemeMusicUrl': profileThemeMusicUrl,
        'isOnlineMsg': isOnlineMsg,
        'isOfflineMsg': isOfflineMsg,
        'uploadCount': uploadCount,
        'followersCount': followersCount,
        'followingCount': followingCount,
        'friendsCount': friendsCount,
        'likesGiven': likesGiven,
        'postsUploaded': postsUploaded,
        'commentsPosted': commentsPosted,
        'dislikesGiven': dislikesGiven,
        'lastUpdated': lastUpdated.toIso8601String(),
        'isFollowing': isFollowing,
      };

  factory ProfileEntity.fromJson(Map<String, dynamic> json) {
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
      isFollowing: json['isFollowing'] as bool? ?? null,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is ProfileEntity &&
          runtimeType == other.runtimeType &&
          userId == other.userId;

  @override
  int get hashCode => userId.hashCode;
}
