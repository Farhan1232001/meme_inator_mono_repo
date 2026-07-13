import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
import 'package:meme_inator_front/core/results.dart';
import 'package:meme_inator_front/features/notifications/data/models/repositories/mock_notification_repo.dart';
import 'package:meme_inator_front/features/notifications/domain/entities/notification_entity.dart';
import 'package:meme_inator_front/features/notifications/domain/enums/notification_type.dart';
import 'package:meme_inator_front/features/notifications/domain/repositories/notification_repository.dart';

class NotificationsView extends StatefulWidget {
  const NotificationsView({super.key});

  @override
  State<NotificationsView> createState() => _NotificationsViewState();
}

class _NotificationsViewState extends State<NotificationsView> {
  final INotificationsRepository _repository = MockNotificationRepository();
  List<NotificationEntity> _allNotifications = [];
  List<NotificationEntity> _filteredNotifications = [];
  bool _isLoading = true;
  NotificationType? _activeFilter;

  @override
  void initState() {
    super.initState();
    _loadNotifications();
  }

  Future<void> _loadNotifications() async {
    setState(() => _isLoading = true);
    try {
      final notificationsResult = await _repository.getNotifications();

      List<NotificationEntity> notifications = notificationsResult.match(
        ok: (value) {return value;},
        notOk: (NotOk<List<NotificationEntity>> notOk) {return [];},
        error: (Error<List<NotificationEntity>> error) {return [];},
      );

      setState(() {
        _allNotifications = notifications;
        _applyFilter();
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      // In a real app, show error dialog or snackbar
    }
  }

  void _applyFilter() {
    if (_activeFilter == null) {
      _filteredNotifications = List.from(_allNotifications);
    } else {
      _filteredNotifications = _allNotifications
          .where((n) => n.notificationType == _activeFilter)
          .toList();
    }
    setState(() {});
  }

  void _setFilter(NotificationType? filter) {
    _activeFilter = filter;
    _applyFilter();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _PlatformFilterCarousel(
          activeFilter: _activeFilter,
          onFilterSelected: _setFilter,
        ),
        Expanded(
          child: _buildContent(),
        ),
      ],
    );
  }

  Widget _buildContent() {
    if (_isLoading) {
      return const Center(child: PlatformCircularProgressIndicator());
    }
    if (_filteredNotifications.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.notifications_none,
              size: 64,
              color: Colors.grey.shade400,
            ),
            const SizedBox(height: 16),
            PlatformText(
              _activeFilter == null
                  ? 'No notifications yet'
                  : 'No ${_activeFilter!.value.toLowerCase()} notifications',
            ),
          ],
        ),
      );
    }
    return RefreshIndicator.adaptive(
      onRefresh: _loadNotifications,
      child: ListView.builder(
        padding: const EdgeInsets.symmetric(vertical: 8),
        itemCount: _filteredNotifications.length,
        itemBuilder: (context, index) {
          final notification = _filteredNotifications[index];
          return _PlatformNotificationTile(notification: notification);
        },
      ),
    );
  }
}

/// Platform-aware filter carousel using Cupertino on iOS, Material on Android
/// Platform-aware filter carousel using Cupertino on iOS, Material on Android
class _PlatformFilterCarousel extends StatelessWidget {
  final NotificationType? activeFilter;
  final void Function(NotificationType?) onFilterSelected;

  const _PlatformFilterCarousel({
    required this.activeFilter,
    required this.onFilterSelected,
  });

  @override
  Widget build(BuildContext context) {
    final filters = [
      FilterOption(icon: Icons.inbox, label: 'All', value: null),
      FilterOption(
        icon: Icons.person_add,
        label: 'Friend Requests',
        value: NotificationType.friendRequest,
      ),
      FilterOption(
        icon: Icons.thumb_up,
        label: 'Likes',
        value: NotificationType.like,
      ),
      FilterOption(
        icon: Icons.thumb_down,
        label: 'Dislikes',
        value: NotificationType.dislike,
      ),
      FilterOption(
        icon: Icons.comment,
        label: 'Comments',
        value: NotificationType.comment,
      ),
    ];

    return PlatformWidget(
      material: (_, __) => _MaterialFilterCarousel(
        filters: filters,
        activeFilter: activeFilter,
        onFilterSelected: onFilterSelected,
      ),
      cupertino: (_, __) => _CupertinoFilterCarousel(
        filters: filters,
        activeFilter: activeFilter,
        onFilterSelected: onFilterSelected,
      ),
    );
  }
}

/// Material Design filter carousel (Android)
class _MaterialFilterCarousel extends StatelessWidget {
  final List<FilterOption> filters;
  final NotificationType? activeFilter;
  final void Function(NotificationType?) onFilterSelected;

  const _MaterialFilterCarousel({
    required this.filters,
    required this.activeFilter,
    required this.onFilterSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      child: Row(
        children: filters.asMap().entries.map((entry) {
          final index = entry.key;
          final filter = entry.value;
          final isActive = activeFilter == filter.value;
          
          // Calculate flex values: active gets 3, inactive gets 1
          final flexValue = isActive ? 3 : 1;
          
          return Expanded(
            flex: flexValue,
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              curve: Curves.easeInOut,
              margin: EdgeInsets.only(
                left: index == 0 ? 0 : 8,
                right: index == filters.length - 1 ? 0 : 0,
              ),
              child: Material(
                color: Colors.transparent,
                child: InkWell(
                  onTap: () => onFilterSelected(filter.value),
                  borderRadius: BorderRadius.circular(32),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                    decoration: BoxDecoration(
                      color: isActive ? Colors.blue : Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(32),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          filter.icon,
                          size: isActive ? 20 : 18,
                          color: isActive ? Colors.white : Colors.grey.shade700,
                        ),
                        if (isActive) ...[
                          const SizedBox(width: 8),
                          AnimatedDefaultTextStyle(
                            duration: const Duration(milliseconds: 200),
                            style: const TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w600,
                              color: Colors.white,
                            ),
                            child: Text(filter.label),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }
}

/// iOS-style filter carousel
class _CupertinoFilterCarousel extends StatelessWidget {
  final List<FilterOption> filters;
  final NotificationType? activeFilter;
  final void Function(NotificationType?) onFilterSelected;

  const _CupertinoFilterCarousel({
    required this.filters,
    required this.activeFilter,
    required this.onFilterSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      child: Row(
        children: filters.asMap().entries.map((entry) {
          final index = entry.key;
          final filter = entry.value;
          final isActive = activeFilter == filter.value;
          
          // Calculate flex values: active gets 3, inactive gets 1
          final flexValue = isActive ? 3 : 1;
          
          return Expanded(
            flex: flexValue,
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              curve: Curves.easeInOut,
              margin: EdgeInsets.only(
                left: index == 0 ? 0 : 8,
                right: index == filters.length - 1 ? 0 : 0,
              ),
              child: CupertinoButton(
                padding: EdgeInsets.zero,
                onPressed: () => onFilterSelected(filter.value),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                  decoration: BoxDecoration(
                    color: isActive 
                        ? CupertinoColors.activeBlue
                        : CupertinoColors.lightBackgroundGray,
                    borderRadius: BorderRadius.circular(32),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        filter.icon,
                        size: isActive ? 20 : 18,
                        color: isActive 
                            ? CupertinoColors.white
                            : CupertinoColors.systemGrey,
                      ),
                      if (isActive) ...[
                        const SizedBox(width: 8),
                        AnimatedDefaultTextStyle(
                          duration: const Duration(milliseconds: 200),
                          style: const TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                            color: CupertinoColors.white,
                          ),
                          child: Text(filter.label),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }
}

/// Platform-aware notification tile
class _PlatformNotificationTile extends StatelessWidget {
  final NotificationEntity notification;

  const _PlatformNotificationTile({required this.notification});

  String _formatDate(DateTime date) {
    final now = DateTime.now();
    final difference = now.difference(date);
    if (difference.inDays > 7) {
      return '${date.day}/${date.month}/${date.year}';
    } else if (difference.inDays > 0) {
      return '${difference.inDays}d ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    } else {
      return 'Just now';
    }
  }

  IconData _getTypeIcon(NotificationType type) {
    switch (type) {
      case NotificationType.like:
        return Icons.thumb_up_alt_outlined;
      case NotificationType.dislike:
        return Icons.thumb_down_alt_outlined;
      case NotificationType.comment:
        return Icons.comment_outlined;
      case NotificationType.friendRequest:
        return Icons.person_add_alt_1;
      default:
        return Icons.notifications_outlined;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      decoration: BoxDecoration(
        color: notification.isRead ? null : Colors.blue.shade50,
        borderRadius: BorderRadius.circular(12),
      ),
      child: PlatformWidget(
        material: (_, __) => Material(
          color: Colors.transparent,
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: Theme.of(context).primaryColor.withOpacity(0.1),
              child: Icon(
                _getTypeIcon(notification.notificationType),
                color: Theme.of(context).primaryColor,
              ),
            ),
            title: Text(
              notification.message,
              style: TextStyle(
                fontWeight: notification.isRead
                    ? FontWeight.normal
                    : FontWeight.w600,
              ),
            ),
            subtitle: Text(
              _formatDate(notification.createdAt),
              style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
            ),
            trailing: notification.isRead
                ? null
                : Container(
                    width: 10,
                    height: 10,
                    decoration: const BoxDecoration(
                      color: Colors.blue,
                      shape: BoxShape.circle,
                    ),
                  ),
            onTap: () {
              // Mark as read action would go here
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Tapped: ${notification.message}')),
              );
            },
          ),
        ),
        cupertino: (_, __) => CupertinoButton(
          padding: EdgeInsets.zero,
          onPressed: () {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Tapped: ${notification.message}')),
            );
          },
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: notification.isRead ? null : CupertinoColors.systemBlue.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              children: [
                CircleAvatar(
                  backgroundColor: CupertinoColors.activeBlue.withOpacity(0.1),
                  child: Icon(
                    _getTypeIcon(notification.notificationType),
                    color: CupertinoColors.activeBlue,
                    size: 20,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        notification.message,
                        style: TextStyle(
                          fontSize: 15,
                          fontWeight: notification.isRead
                              ? FontWeight.normal
                              : FontWeight.w600,
                          color: CupertinoColors.label,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        _formatDate(notification.createdAt),
                        style: TextStyle(
                          fontSize: 12,
                          color: CupertinoColors.secondaryLabel,
                        ),
                      ),
                    ],
                  ),
                ),
                if (!notification.isRead)
                  Container(
                    width: 8,
                    height: 8,
                    decoration: BoxDecoration(
                      color: CupertinoColors.activeBlue,
                      shape: BoxShape.circle,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class FilterOption {
  final IconData icon;
  final String label;
  final NotificationType? value;
  FilterOption({required this.icon, required this.label, this.value});
}