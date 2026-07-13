class MenuState {
  final int selectedIndex;
  final bool isMenuOpen;

  const MenuState({
    required this.selectedIndex,
    required this.isMenuOpen,
  });

  factory MenuState.initial() {
    return const MenuState(
      selectedIndex: 0,
      isMenuOpen: false,
    );
  }

  MenuState copyWith({
    int? selectedIndex,
    bool? isMenuOpen,
  }) {
    return MenuState(
      selectedIndex: selectedIndex ?? this.selectedIndex,
      isMenuOpen: isMenuOpen ?? this.isMenuOpen,
    );
  }
}