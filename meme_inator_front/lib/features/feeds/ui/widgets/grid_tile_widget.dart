// import 'package:flutter/material.dart';
// import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
// import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';


// // TODO: Make this widget platform aware
// class GridTileWidget extends StatelessWidget {
//   const GridTileWidget({Key? key, required PostEntity post, this.onTap})
//       : _post = post,
//         super(key: key);
//   final PostEntity _post;
//   final VoidCallback? onTap;

//   @override
//   Widget build(BuildContext context) {
//     final theme = Theme.of(context);
//     final imagePlaceholder = Image.asset(
//       'assets/images/No-Image_Icon.svg',
//       fit: BoxFit.cover,
//     );
//     return GestureDetector(
//       onTap: onTap,
//       child: PlatformWidget(
//         cupertino: (_, __) => GridTile(
//           child: SizedBox(
//             height: 300,
//             width: 300,
//             child: _post.thumbnailUrl!.isNotEmpty
//                 ? Image.network(
//                     _post.thumbnailUrl ?? '',
//                     fit: BoxFit.fill,
//                     errorBuilder: (context, error, stackTrace) {
//                       return Image.asset(
//                         'assets/images/No-Image_Icon.svg',
//                         fit: BoxFit.cover,
//                       );
//                     },
//                   )
//                 : const SizedBox.shrink(),
//           ),
//         ),
//         material: (_, __) => GridTile(
//           child: Container(
//             height: 300,
//             width: 300,
//             child: _post.thumbnailUrl!.isNotEmpty
//                 ? Image.network(
//                     _post.thumbnailUrl!,
//                     fit: BoxFit.fill,
//                     errorBuilder: (context, error, stackTrace) {
//                       return Image.asset(
//                         'assets/images/No-Image_Icon.svg',
//                         fit: BoxFit.cover,
//                       );
//                     },
//                   )
//                 : const SizedBox.shrink(),
//           ),
//         ),
//       ),
//     );
//   }
// }
