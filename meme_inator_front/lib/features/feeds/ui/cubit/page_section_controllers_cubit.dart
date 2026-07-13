// // lib/features/feeds/ui/cubit/page_section_controllers_cubit.dart

// // ignore_for_file: sort_constructors_first

// import 'package:flutter/widgets.dart';
// import 'package:flutter_bloc/flutter_bloc.dart';
// import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
// import 'package:meme_inator_front/features/post/domain/entities/post_entity.dart';


// // Holds references for controlleres OWNED by a SectionalFeedContent. 
// // TODO: Turn this into a class
// class SectionalFeedControllersCubit extends Cubit<PageSectionControllersState> {
//   PagingController<String, PostEntity>? _pagingController;
//   ScrollController? _listController;

//   SectionalFeedControllersCubit({
//     PagingController<String, PostEntity>? pagingController,
//     ScrollController? listController,
//   })  : _pagingController = pagingController,
//         _listController = listController,
//         super(PageSectionControllersState(
//           pagingController: pagingController,
//           listController: listController,
//         ));

//   PagingController<String, PostEntity>? get pagingController => _pagingController;
//   ScrollController? get listController => _listController;

//   void updateControllers({
//     PagingController<String, PostEntity>? pagingController,
//     ScrollController? listController,
//   }) {
//     _pagingController = pagingController ?? _pagingController;
//     _listController = listController ?? _listController;
//     emit(PageSectionControllersState(
//       pagingController: pagingController ?? _pagingController,
//       listController: listController ?? _listController,
//     ));
//   }

//   @override
//   Future<void> close() {
//     _pagingController?.dispose(); _pagingController = null;
//     _listController?.dispose();   _listController = null;
//     return super.close();
//   }
// }

// // post_controllers_state.dart

// /// Controllers that need to be shared across 
// /// page_section related widgets ie widgets that
// /// are related to make feeds with sections of GridViews
// class PageSectionControllersState {
//   final PagingController<String, PostEntity>? pagingController;
//   final ScrollController? listController;

//   const PageSectionControllersState({
//     required this.pagingController,
//     required this.listController,
//   });
// }
