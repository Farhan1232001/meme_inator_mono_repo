import 'package:equatable/equatable.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

/// Duration window value object (one bucket of posts)
class DurationWindowVo extends Equatable {
  final String label;
  final DateTime startDate;
  final DateTime endDate;
  final List<PostEntity> posts;

  const DurationWindowVo({
    required this.label,
    required this.startDate,
    required this.endDate,
    required this.posts,
  });

  @override
  List<Object?> get props => [label, startDate, endDate, posts];
}
