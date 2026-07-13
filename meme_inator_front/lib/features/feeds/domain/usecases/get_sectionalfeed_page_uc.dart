import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_request_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_response_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/repositories/ifeed_repository.dart';

class GetSectionalFeedUseCase 
    implements IUseCase<SectionalFeedPageRequestVo, SectionalFeedPageResponseVo> {
  final IFeedRepository _repository;

  GetSectionalFeedUseCase(this._repository);

  @override
  Future<Result<SectionalFeedPageResponseVo>> execute({required SectionalFeedPageRequestVo valObj}) async { 
    return await _repository.getSectionalFeed(valObj);
  }
}
