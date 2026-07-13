// lib/features/feeds/data/models/repositories/feed_repository_impl.dart
import 'package:dio/dio.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/feeds/data/models/services/remote/feeds_api_service.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/feed_page_response.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_request_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_response_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_request_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_response_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/repositories/ifeed_repository.dart';
import 'package:meme_inator_front/features/feeds/feeds_mapper.dart';

class FeedRepositoryImpl implements IFeedRepository {
  final FeedsApiService _apiService;

  ///TODO: To hold nextCursor, just hold it as string, not as entire response vo. 
  /// Holds nextCursor from the last response
  FeedPageResponseVo? lastPagedResponseVo;

  FeedRepositoryImpl(this._apiService);

  @override
  Future<Result<GridFeedPageResponseVo>> getGridFeed(
    GridfeedPageRequestVo request,
  ) async {
    try {
      final response = await _apiService.getGridFeed(
        feedType: request.gridFeedType.value, // Backend expects 'type' not 'feed_type'
        cursor: request.cursor,
        pageSize: request.pageSize,
        requestingUserId: request.requestingUserId,
        authorUsername: request.authorUsername,  
      );

      final responseVo = FeedsMapper.mapGridFeedDtoToVo(response);
      lastPagedResponseVo = responseVo;

      return Ok(responseVo);
    } on DioException catch (e) {
      return _handleDioError(e);
    } catch (e) {
      return Error.fromException(
        e is Exception ? e : Exception(e.toString()),
        message: 'Failed to fetch grid feed',
      );
    }
  }

  @override
  Future<Result<SectionalFeedPageResponseVo>> getSectionalFeed(
    SectionalFeedPageRequestVo request,
  ) async {
    try {
      final response = await _apiService.getSectionalFeed(
        feedType: request.sectionalFeedType.value, // Backend expects 'feed_type'
        durationUnit: request.durationUnit,
        durationWindowSize: request.durationWindowSize,
        cursor: request.cursor,
        requestingUserId: request.requestingUserId,
        authorUsername: request.authorUsername,  
      );

      final responseVo = FeedsMapper.mapSectionalFeedDtoToVo(response);
      lastPagedResponseVo = responseVo;
      
      return Ok(responseVo);
    } on DioException catch (e) {
      return _handleDioError(e);
    } catch (e) {
      return Error.fromException(
        e is Exception ? e : Exception(e.toString()),
        message: 'Failed to fetch sectional feed',
      );
    }
  }

  void clearLastPagedResponse() {
    lastPagedResponseVo = null;
  }

  //TODO: should be in /core
  Result<T> _handleDioError<T>(DioException e) {
    if (e.type == DioExceptionType.connectionTimeout ||
        e.type == DioExceptionType.sendTimeout ||
        e.type == DioExceptionType.receiveTimeout) {
      return Error.timeout(
        message: 'Request timeout. Please check your connection.',
        exception: e,
      );
    } else if (e.type == DioExceptionType.connectionError) {
      return Error.networkError(
        message: 'Network error. Please check your internet connection.',
        exception: e,
      );
    } else if (e.response != null) {
      // Handle HTTP error codes
      final statusCode = e.response!.statusCode;
      final responseData = e.response?.data;

      // Safely extract error message
      String? errorMessage;
      if (responseData is Map<String, dynamic>) {
        errorMessage = responseData['message']?.toString();
      } else if (responseData is String) {
        errorMessage = responseData;
      }

      // Use the DioException message as fallback
      errorMessage ??= e.message;

      switch (statusCode) {
        case 400:
          return NotOk.badRequest(message: errorMessage);
        case 401:
          return NotOk.unauthorized(message: errorMessage);
        case 403:
          return NotOk.forbidden(message: errorMessage);
        case 404:
          return NotOk.notFound(message: errorMessage);
        case 409:
          return NotOk.conflict(message: errorMessage);
        case 422:
          return NotOk.validationError(message: errorMessage);
        default:
          return Error(
            message: errorMessage ?? 'Server error',
            statusCode: statusCode ?? 500,
            exception: e,
          );
      }
    } else {
      return Error.fromException(
        e,
        message: 'Network request failed',
      );
    }
  }
}
