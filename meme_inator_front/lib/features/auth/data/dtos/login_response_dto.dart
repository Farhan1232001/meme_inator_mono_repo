import 'package:json_annotation/json_annotation.dart';
part 'login_response_dto.g.dart';

@JsonSerializable(createToJson: true)
class LoginResponseDto {
  @JsonKey(name: 'access')
  final String access;
  
  @JsonKey(name: 'refresh')
  final String refresh;

  LoginResponseDto({
    required this.access,
    required this.refresh,
  });

  factory LoginResponseDto.fromJson(Map<String, dynamic> json) =>
      _$LoginResponseDtoFromJson(json);

  Map<String, dynamic> toJson() => _$LoginResponseDtoToJson(this);
}