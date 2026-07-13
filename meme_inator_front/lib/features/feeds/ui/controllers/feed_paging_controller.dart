import 'dart:collection';
import 'package:flutter/material.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

typedef FeedPageFetcher =
    Future<Result<FeedPageResponse>> Function(String? cursor);

class FeedPageResponse {
  final List<PostEntity> items;
  final String? nextCursor;

  FeedPageResponse({required this.items, this.nextCursor});
}

/// Manages paging for any feed (grid or sectional).
/// For sectional feeds, you can enable caching and handle multiple sections per page.
/// 
/// Why create this class? I wanted to use FeedViewModel's feedpaging logic
/// inside ProfileViewModel but didnt want duplicate code. 
class FeedPagingController {
  late final PagingController<String, PostEntity> pagingController;
  late final ScrollController scrollController;
  final FeedPageFetcher fetchPageFn;
  final bool isSectional;
  final ListQueue<List<PostEntity>> _cacheQueue = ListQueue();
  String? _nextCursor;

  FeedPagingController({
    required this.fetchPageFn,
    this.isSectional = false,
  }) {
    pagingController = PagingController<String, PostEntity>(
      getNextPageKey: _getNextCursor,
      fetchPage: _fetchPage,
    );
    scrollController = ScrollController();
  }

  String? _getNextCursor(PagingState<String, PostEntity> state) {
    // If no more pages, return null
    return _nextCursor;
  }

  Future<List<PostEntity>> _fetchPage(String cursor) async {
    // If we have cached sections, return the first one
    if (isSectional && _cacheQueue.isNotEmpty) {
      return _cacheQueue.removeFirst();
    }

    final result = await fetchPageFn(cursor.isEmpty ? null : cursor);
    switch (result) {
      case Ok<FeedPageResponse>():
        final response = result.value;
        _nextCursor = response.nextCursor;

        if (isSectional) {
          // For sectional feeds, response.items might be a list of sections.
          // We'll assume each section is a list of posts, and we cache extras.
          // This requires the fetcher to return a FeedPageResponse where items
          // is actually a list of lists (List<List<PostEntity>>). For simplicity,
          // we'll keep it generic and let the caller handle sectioning.
          // In practice, you'd pass a custom mapper.
          // For now, we just return items as a flat list.
          return response.items;
        } else {
          return response.items;
        }

      case NotOk<FeedPageResponse>():
        throw Exception(result.message); // paging controller will catch
      case Error<FeedPageResponse>():
        throw Exception(result.message);
    }
  }

  void refresh() {
    _nextCursor = null;
    _cacheQueue.clear();
    pagingController.refresh();
  }

  void dispose() {
    pagingController.dispose();
    scrollController.dispose();
  }
}
