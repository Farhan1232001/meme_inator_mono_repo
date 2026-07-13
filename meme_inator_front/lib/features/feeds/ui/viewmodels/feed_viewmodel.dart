// lib/features/feeds/ui/viewmodels/feed_viewmodel.dart
// ignore_for_file: sort_constructors_first, unnecessary_this

import 'dart:collection';

import 'package:flutter/widgets.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:meme_inator_front/core/iusecase.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/feeds/data/models/repositories/feed_repository_impl.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_request_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/gridfeed_page_response_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_request_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/entities/value_objects/sectionalfeed_page_response_vo.dart';
import 'package:meme_inator_front/features/feeds/domain/repositories/ifeed_repository.dart';
import 'package:meme_inator_front/features/feeds/domain/usecases/get_gridfeed_page_uc.dart';
import 'package:meme_inator_front/features/feeds/domain/usecases/get_sectionalfeed_page_uc.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/feeds/ui/cubit/feed_states.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

/// PagingController is SSOT for posts
/// cubit state responsible for initial loading/error statusCode
///
/// The refresh and fetchPage methods in this class
/// are passed in as callbacks into the pagingController.
class FeedViewModel extends Cubit<FeedState> {
  final IFeedRepository _feedRepository;
  final FeedConfig _feedConfig;

  // Initialize controllers immediately with late but don't recreate
  late final ScrollController _listController;
  late final PagingController<String, PostEntity> _pagingController;

  final ListQueue<List<PostEntity>> _cacheQueue = ListQueue();

  // Getters
  ScrollController get listController => _listController;
  PagingController<String, PostEntity> get pagingController =>
      _pagingController;
  FeedConfig get feedConfig => _feedConfig;

  FeedViewModel({
    required FeedConfig feedConfig,
    required IFeedRepository feedRepository,
  }) : _feedConfig = feedConfig,
       _feedRepository = feedRepository,
       super(const FeedInitialState()) {
    // Initialize controllers ONCE
    _listController = ScrollController();
    _pagingController = PagingController<String, PostEntity>(
      getNextPageKey: (pagingState) =>
          getNextCursor(pagingState as PagingState<String, PostEntity>),
      fetchPage: fetchPage,
    );

    // Initialize config
    _initializeForConfig(_feedConfig);

    // Trigger first page load for new feeds
    // DO NOT trigger fetch here - let the UI do it when ready
  }

  void _initializeForConfig(FeedConfig config) {
    late final IUseCase<dynamic, dynamic> getFeedPageUsecase;
    switch (config.type) {
      case FeedType.sectionalFeed:
        getFeedPageUsecase = GetIt.instance.get<GetSectionalFeedUseCase>();
      case FeedType.gridFeed:
        getFeedPageUsecase = GetIt.instance.get<GetGridFeedUseCase>();
      case FeedType.listFeed:
        throw UnimplementedError();
    }
    emit(
      FeedLoadedState(
        config: config,
        type: config.type,
        get_feed_page_usecase: getFeedPageUsecase,
      ),
    );
  }

  @override
  Future<void> close() async {
    _pagingController.dispose();
    _listController.dispose();
    await super.close();
  }

  String? getNextCursor(PagingState<String, PostEntity> pagingState) {
    // null means no more pages
    if (state is! FeedLoadedState) return '';
    final lastPageResponse = _feedRepository.lastPagedResponseVo;
    if (lastPageResponse is SectionalFeedPageResponseVo &&
        lastPageResponse.noMore &&
        _cacheQueue.isEmpty) {
      return null;
    }
    return lastPageResponse?.nextCursor ?? '';
  }

  Future<List<PostEntity>> fetchPage(String nextCursor) async {
    if (state is! FeedLoadedState) return [];

    final feedState = state as FeedLoadedState;
    final feedType = feedState.type;

    // FeedLoadedState emitted inside the specific fetch methods
    switch (feedType) {
      case FeedType.sectionalFeed:
        return _fetchSectionalFeedPage(nextCursor);
      case FeedType.gridFeed:
        return _fetchGridFeedPage(nextCursor);
      case FeedType.listFeed:
        throw UnimplementedError();
    }
  }

  Future<List<PostEntity>> _fetchSectionalFeedPage(String nextCursor) async {
    final feedState = state as FeedLoadedState;
    final feedConfig = feedState.config;
    final getSectionFeedPageUsecase = feedState.get_feed_page_usecase;
    assert(
      getSectionFeedPageUsecase is GetSectionalFeedUseCase,
      '_fetchSectionalFeedPage MUST be of type GetSectionalFeedUseCase ',
    );

    // 0. Check cache.
    // ... Single response can have >1 duration_windows
    // ... A duration window should correspond to ONE section.
    // ... One section should corresponde to ONE "page"
    // ... (page, as defined in context of infinite_scroll_pagination)
    if (_cacheQueue.isNotEmpty) {
      return _cacheQueue.removeFirst();
    }

    // 1. Build Request
    final pageRequest = SectionalFeedPageRequestVo(
      sectionalFeedType: feedConfig.sectionalFeedSubType!,
      durationUnit: feedConfig.durationUnit ?? 'day',
      durationWindowSize:
          feedConfig.durationWindowSize ?? FeedConfig.defaultDurationWindowSize,
      cursor: nextCursor,
      authorUsername: feedConfig.authorUsername,
      requestingUserId: null,
    );

    // 2. Try excecution of usecase
    try {
      final Result<SectionalFeedPageResponseVo> result =
          await getSectionFeedPageUsecase.execute(
                valObj: pageRequest,
              )
              as Result<SectionalFeedPageResponseVo>;

      // 3. Handle Result
      switch (result) {
        case Ok<SectionalFeedPageResponseVo>():
          // 1. Unwarp result type Ok
          // ... A section corresponds to A duration window.
          final sections = result.value.durationWindowsAsLists;
          // ... add extra duration windows ie sections to cache
          for (var i = 1; i < sections.length; i++) {
            if (sections[i].isNotEmpty) {
              _cacheQueue.add(sections[i]);
            }
          }

          return sections[0];

        case NotOk<SectionalFeedPageResponseVo>():
          emit(
            FeedGlobalError(
              statusCode: result.statusCode,
              staticMessage: result.staticMessage,
              message: result.message,
            ),
          );
          throw Exception('${result.staticMessage}: ${result.message}');
          return [];
        case Error<SectionalFeedPageResponseVo>():
          emit(
            FeedGlobalError(
              statusCode: result.statusCode,
              staticMessage: result.staticMessage,
              message: result.message,
              exception: result.exception,
            ),
          );
          throw Exception('${result.staticMessage}: ${result.message}');
          return [];
      }
    } on Exception catch (e) {
      emit(
        const FeedGlobalError(
          statusCode: -1,
          staticMessage: '',
          message: 'feed_viewmodel error',
        ),
      );
      return [];
    }
  }

  Future<List<PostEntity>> _fetchGridFeedPage(String nextCursor) async {
    final feedState = state as FeedLoadedState;
    final feedConfig = feedState.config;
    final getGridFeedPageUsecase = feedState.get_feed_page_usecase;
    assert(
      getGridFeedPageUsecase is GetGridFeedUseCase,
      '_fetchGridFeedPage MUST be of type GetGridFeedUseCase ',
    );

    // 1. Build Request
    final pageRequest = GridfeedPageRequestVo(
      gridFeedType: feedConfig.gridFeedSubType!,
      pageSize: feedConfig.pageSize,
      cursor: nextCursor,
      authorUsername: feedConfig.authorUsername,
      requestingUserId: null,
    );

    // 2. Try excecution of usecase
    try {
      final Result<GridFeedPageResponseVo> result =
          await getGridFeedPageUsecase.execute(
                valObj: pageRequest,
              )
              as Result<GridFeedPageResponseVo>;

      // 3. Handle Result
      switch (result) {
        case Ok<GridFeedPageResponseVo>():
          // Force a tiny delay to let the paging controller settle
          await Future.delayed(Duration.zero);
          return result.value.results;

        case NotOk<GridFeedPageResponseVo>():
          emit(
            FeedGlobalError(
              statusCode: result.statusCode,
              staticMessage: result.staticMessage,
              message: result.message,
            ),
          );
          throw Exception('${result.staticMessage}: ${result.message}');
          return [];
        case Error<GridFeedPageResponseVo>():
          emit(
            FeedGlobalError(
              statusCode: result.statusCode,
              staticMessage: result.staticMessage,
              message: result.message,
              exception: result.exception,
            ),
          );
          throw Exception('${result.staticMessage}: ${result.message}');
          return [];
      }
    } on Exception catch (e) {
      emit(
        const FeedGlobalError(
          statusCode: -1,
          staticMessage: '',
          message: 'feed_viewmodel error',
        ),
      );
      return [];
    }
  }

  Future<void> refreshFeed() async {
    debugPrint('refreshFeed called, state = ${state.runtimeType}');
    debugPrint(
      'refreshFeed called, pages before: ${_pagingController.value.pages?.length}',
    );

    if (state is! FeedLoadedState) return;

    _cacheQueue.clear();
    _pagingController.refresh();
    _feedRepository.lastPagedResponseVo = null;

    await Future.microtask(() {
      _pagingController.fetchNextPage();
    });
  }

  void handleFeedGlobalError() {
    // 1. Re-initialize with same config
    _initializeForConfig(_feedConfig);
  }

  void clearFeedRepository() {
    _feedRepository.clearLastPagedResponse();
  }
}
