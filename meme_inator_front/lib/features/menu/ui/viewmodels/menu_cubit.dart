import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/features/menu/ui/bloc/menu_state.dart';

class MenuCubit extends Cubit<MenuState> {
  MenuCubit() : super(MenuState.initial());

  void selectTab(int index) {
    emit(state.copyWith(selectedIndex: index));
  }

  void nextTab() {
    if (state.selectedIndex < 1) {
      emit(state.copyWith(selectedIndex: state.selectedIndex + 1));
    }
  }

  void previousTab() {
    if (state.selectedIndex > 0) {
      emit(state.copyWith(selectedIndex: state.selectedIndex - 1));
    }
  }
}

