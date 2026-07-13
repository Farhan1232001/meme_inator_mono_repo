// lib/features/menu/domain/entities/menu_item_entity.dart
import 'package:equatable/equatable.dart';

class MenuItemEntity extends Equatable {
  final String title;
  final String iconName;
  final String route;
  final bool requiresAuth;
  
  const MenuItemEntity({
    required this.title,
    required this.iconName,
    required this.route,
    this.requiresAuth = false,
  });
  
  @override
  List<Object?> get props => [title, iconName, route, requiresAuth];
}