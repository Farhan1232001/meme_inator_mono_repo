import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

class PostWidget extends StatelessWidget {
  final PostEntity _post;

  const PostWidget({Key? key, required PostEntity post})
      : _post = post,
        super(key: key);

  @override
  Widget build(BuildContext context) {
    return PlatformWidget(
      material: (_, __) => _buildMaterialCard(),
      cupertino: (_, __) => _buildCupertinoCard(),
    );
  }

  Widget _buildMaterialCard() {
    return SizedBox(
      width: 300,
      height: 300,
      child: Image.network(
        _post.thumbnailUrl ?? '',
        fit: BoxFit.cover,
      ),
    );
  }

  static double get width => 300;
  static double get height => 300;

  Widget _buildCupertinoCard() {
    return SizedBox(
      width: 300,
      height: 300,
      child: Image.network(
        _post.thumbnailUrl ?? '',
        fit: BoxFit.cover,
      ),
    );
  }
}
