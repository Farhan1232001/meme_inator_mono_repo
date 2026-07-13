// main_production.dart
// import 'package:meme_inator0/app/app.dart';
// import 'package:meme_inator0/bootstrap.dart';
import 'package:meme_inator_front/app/view/app.dart';
import 'package:meme_inator_front/bootstrap.dart';

Future<void> main() async {
  await bootstrap(() => const App());
}
