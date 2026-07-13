// lib/core/iusecase.dart
// ignore_for_file: avoid_types_as_parameter_names, one_member_abstracts

import 'package:meme_inator_front/core/results.dart';

abstract class IUseCase<InputVo, OutputVo> {
  Future<Result<OutputVo>> execute({required InputVo valObj});
}
