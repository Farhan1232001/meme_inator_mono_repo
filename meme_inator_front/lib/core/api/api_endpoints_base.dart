// /lib/core/api/api_endpoints_base.dart
// ignore_for_file: use_setters_to_change_properties

import 'package:meme_inator_front/core/api/enums/environment.dart';

/// Base URL and utility functions for API endpoints
class ApiEndpointsBase {
  /// TODO: Envionrment should be a CONST, should not be able to change during runtime.
  static Environment _currentEnvironment = Environment.development;

  // Base URLs
  static String developmentBaseUrl = 'http://localhost:8000';
  static const String stagingBaseUrl = 'https://staging.meme-inator.com';
  static const String productionBaseUrl = 'https://meme-inator.com';

  // API version prefix
  static const String apiPrefix = '/api/v0';

  // Set the development URL (call this before any API usage)
  static void setDevelopmentBaseUrl(String url) {
    developmentBaseUrl = url;
  }
  // Helper method to build full URLs
  static String buildUrl(
    String path, {
    Environment environment = Environment.development,
  }) {
    final baseUrl = getBaseUrl(environment);
    return '$baseUrl$apiPrefix$path';
  }

  static String getCurrentBaseUrl() {
    switch (_currentEnvironment) {
      case Environment.production:
        return productionBaseUrl;
      case Environment.staging:
        return stagingBaseUrl;
      case Environment.development:
        return developmentBaseUrl;
    }
  }

  static String getBaseUrl(Environment environment) {
    switch (environment) {
      case Environment.production:
        return productionBaseUrl;
      case Environment.staging:
        return stagingBaseUrl;
      case Environment.development:
        return developmentBaseUrl;
    }
  }

  // Set the current environment (should be called early in app startup)
  static void setEnvironment(Environment environment) {
    _currentEnvironment = environment;
  }
}
