// main_development.dart
// import 'package:meme_inator0/app/app.dart';
// import 'package:meme_inator0/bootstrap.dart';
import 'package:meme_inator_front/app/view/app.dart';
import 'package:meme_inator_front/bootstrap.dart';
import 'package:meme_inator_front/core/api/api_endpoints_base.dart';
import 'package:meme_inator_front/core/api/enums/environment.dart';

Future<void> main() async {
  // Setup ApiEndpoints for Development Flavor
  const baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );
  ApiEndpointsBase.setDevelopmentBaseUrl(baseUrl);
  ApiEndpointsBase.setEnvironment(Environment.development);
  await bootstrap(() => const App());
}
