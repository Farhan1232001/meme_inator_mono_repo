import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_request_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_response_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/repositories/ifeed_repository.dart';

class GetGridFeedUseCase 
    implements IUseCase<GridfeedPageRequestVo, GridFeedPageResponseVo> {
  final IFeedRepository _repository;

  GetGridFeedUseCase(this._repository);

  @override
  Future<Result<GridFeedPageResponseVo>> execute({
    required GridfeedPageRequestVo valObj // Use valObj to match IUseCase signature
  }) async {
    return await _repository.getGridFeed(valObj);
  }
}
