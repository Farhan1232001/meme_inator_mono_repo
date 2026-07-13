import 'package:dio/dio.dart';
import 'package:meme_inator_front/features/users/data/dtos/user_dto.dart';
import 'package:retrofit/retrofit.dart';

part 'user_api_service.g.dart';

@RestApi()
abstract class UserApiService {
  factory UserApiService(Dio dio, {String baseUrl}) = _UserApiService;

  @POST('/users/{user_id}/follow')
  Future<void> followUser(@Path('user_id') String userId);

  @DELETE('/users/{user_id}/unfollow')
  Future<void> unfollowUser(@Path('user_id') String userId);

  @GET('/users/{username}')
  Future<UserDto> getUserByUsername(@Path('username') String username);

  @GET('/users/me')
  Future<UserDto> getUserByToken();
}
