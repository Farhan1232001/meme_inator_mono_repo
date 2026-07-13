
import 'package:meme_inator_front/features/users/domain/entities/user_entity.dart';
import 'package:meme_inator_front/features/users/data/dtos/user_dto.dart';


class UsersMapper {
  /// Convert UserDto to UserEntity
  static UserEntity dtoToEntity(UserDto dto) {
    return UserEntity(
      id: dto.id,
      username: dto.username,
      email: dto.email,
      isOnline: dto.isOnline,
      isProUser: dto.isProUser,
      isVerified: dto.isVerified,
      isBanned: dto.isBanned,
    );
  }

  /// Convert UserEntity to UserDto
  static UserDto entityToDto(UserEntity entity) {
    return UserDto(
      id: entity.id,
      email: entity.email,
      username: entity.username,
      isOnline: entity.isOnline,
      isProUser: entity.isProUser,
      isVerified: entity.isVerified,
      isBanned: entity.isBanned,
    );
  }
}