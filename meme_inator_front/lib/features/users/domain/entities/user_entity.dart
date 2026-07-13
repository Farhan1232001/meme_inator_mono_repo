import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:uuid/uuid.dart';

class UserEntity {
    final UuidValue id;
    final String username;
    final String email;

    final bool isOnline;
    // Now attribute of an Entitlement
    final bool isProUser;
    final bool isVerified;
    final bool isBanned;

    final DateTime dateJoined;

    final ProfileEntity? profile;
    final bool isSoftDeleted;

    UserEntity({
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
}


