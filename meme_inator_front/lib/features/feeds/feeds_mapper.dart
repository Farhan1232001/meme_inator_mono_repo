import 'package:meme_inator_front/features/post/posts_mapper.dart';
import 'package:meme_inator_front/features/feeds/data/dtos/duration_window_dto.dart';
import 'package:meme_inator_front/features/feeds/data/dtos/gridfeed_page_response_dto.dart';
import 'package:meme_inator_front/features/feeds/data/dtos/sectionalfeed_page_response_dto.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/duration_window_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_response_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_response_vo.dart';

class FeedsMapper {
  /// Convert GridFeedPageResponseDto to GridFeedPageResponseVo
  static GridFeedPageResponseVo mapGridFeedDtoToVo(
    GridFeedPageResponseDto dto,
  ) {
    return GridFeedPageResponseVo(
      nextCursor: dto.nextCursor,
      results: dto.results.map(PostsMapper.dtoToEntity).toList(),
    );
  }

  /// Convert SectionalFeedPageResponseDto to SectionalFeedPageResponseVo
  static SectionalFeedPageResponseVo mapSectionalFeedDtoToVo(
    SectionalFeedPageResponseDto dto,
  ) {
    return SectionalFeedPageResponseVo(
      durationWindows: dto.durationWindows
          .map((windowDto) => _mapDurationWindowDtoToVo(windowDto))
          .toList(),
      nextCursor: dto.nextCursor,
      hasMore: dto.hasMore,
    );
  }

  /// Convert DurationWindowDto to DurationWindowVo
  static DurationWindowVo _mapDurationWindowDtoToVo(
    DurationWindowDto dto,
  ) {
    return DurationWindowVo(
      label: dto.label,
      startDate: dto.startDate,
      endDate: dto.endDate,
      posts: dto.posts.map(PostsMapper.dtoToEntity).toList(),
    );
  }

  /// Convert GridFeedPageResponseVo to GridFeedPageResponseDto
  static GridFeedPageResponseDto mapGridFeedVoToDto(
    GridFeedPageResponseVo vo,
  ) {
    return GridFeedPageResponseDto(
      nextCursor: vo.nextCursor,
      results: vo.results.map(PostsMapper.entityToDto).toList(),
    );
  }

  /// Convert SectionalFeedPageResponseVo to SectionalFeedPageResponseDto
  static SectionalFeedPageResponseDto mapSectionalFeedVoToDto(
    SectionalFeedPageResponseVo vo,
  ) {
    return SectionalFeedPageResponseDto(
      durationWindows: vo.durationWindows
          .map((windowVo) => _mapDurationWindowVoToDto(windowVo))
          .toList(),
      nextCursor: vo.nextCursor,
      hasMore: vo.hasMore,
    );
  }

  /// Convert DurationWindowVo to DurationWindowDto
  static DurationWindowDto _mapDurationWindowVoToDto(
    DurationWindowVo vo,
  ) {
    return DurationWindowDto(
      label: vo.label,
      startDate: vo.startDate,
      endDate: vo.endDate,
      posts: vo.posts.map(PostsMapper.entityToDto).toList(),
    );
  }

  /// Convert DTO to Entity (alias for mapGridFeedDtoToEntity)
  static GridFeedPageResponseVo dtoToVo(GridFeedPageResponseDto dto) {
    return mapGridFeedDtoToVo(dto);
  }

  /// Convert Entity to DTO (alias for mapGridFeedEntityToDto)
  static GridFeedPageResponseDto valobjToDto(GridFeedPageResponseVo entity) {
    return mapGridFeedVoToDto(entity);
  }

  /// Convert Sectional DTO to Entity
  static SectionalFeedPageResponseVo sectionalDtoToVo(
    SectionalFeedPageResponseDto dto,
  ) {
    return mapSectionalFeedDtoToVo(dto);
  }

  /// Convert Sectional Entity to DTO
  static SectionalFeedPageResponseDto sectionalVoToDto(
    SectionalFeedPageResponseVo entity,
  ) {
    return mapSectionalFeedVoToDto(entity);
  }
}
