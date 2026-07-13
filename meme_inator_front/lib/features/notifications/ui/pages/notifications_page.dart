import 'package:flutter/material.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:meme_inator_front/features/notifications/ui/views/notifications_view.dart';

class NotificationsPage extends StatelessWidget {
  const NotificationsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return PlatformScaffold(
      appBar: _buildAppBar(),
      body: const NotificationsView(),
    );
  }

  PlatformAppBar _buildAppBar() {
    return const PlatformAppBar(
      title: Text('Notifications'),
    );
  }
}

