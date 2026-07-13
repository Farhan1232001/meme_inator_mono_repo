import 'package:json_annotation/json_annotation.dart';
part 'login_request_dto.g.dart';

@JsonSerializable(createToJson: true)
class LoginRequestDto {
  @JsonKey(name: 'usernameOrEmail')
  final String usernameOrEmail;
  
  @JsonKey(name: 'password')
  final String password;

  @JsonKey(name: 'remember_me')
  final bool rememberMe;

  LoginRequestDto({
    required this.usernameOrEmail,
    required this.password,
    required this.rememberMe
  });

  factory LoginRequestDto.fromJson(Map<String, dynamic> json) =>
      _$LoginRequestDtoFromJson(json);

  Map<String, dynamic> toJson() => _$LoginRequestDtoToJson(this);
}
