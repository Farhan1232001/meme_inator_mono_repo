import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';

class PostPageViewWidget extends StatelessWidget {
  final PostEntity post;

  const PostPageViewWidget({super.key, required this.post});

  @override
  Widget build(BuildContext context) {
    final theme = PlatformTheme.of(context); // need to use this below
    return SafeArea(
      child: Column(
        children: [
          // Header
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Container(),
          ),

          // Post content
          Expanded(
            child: Center(
              child: Image.network(post.imageUrl),
            ),
          ),
        ],
      ),
    );
  }
}
