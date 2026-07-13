// lib/features/feeds/ui/cubits/section_heights_cache.dart
import 'package:flutter_bloc/flutter_bloc.dart';

/// Height of each entire section recorded (including header/footer if included), in pixels
class SectionHeightsCacheCubit extends Cubit<List<double?>> {
  SectionHeightsCacheCubit() : super(List.filled(100, null, growable: true));

  void setSectionHeight(int sectionIndex, double height) {
    final heights = List<double?>.from(state);
    if (sectionIndex >= heights.length) {
      heights.length = sectionIndex + 100;
    }
    heights[sectionIndex] = height;
    emit(heights);
  }

  List<double?> get sectionHeightsList => List.unmodifiable(state);

  // to index excluded
  double? getCumulatedHeight(int from, int to) {
    if (from < 0 || to >= state.length || from > to) return null;
    double sum = 0.0;
    for (int i = from; i < to; i++) {
      final sectionHeight = state[i];
      if (sectionHeight == null) return null;
      sum += sectionHeight;
    }
    return sum;
  }

  double? getSectionHeight(int index) {
    if (index < 0 || index >= state.length) return null;
    return state[index];
  }

  double get totalHeight => state.whereType<double>().fold(0.0, (a, b) => a + b);

  void clear() {
    emit(List.filled(100, null, growable: true));
  }
}
