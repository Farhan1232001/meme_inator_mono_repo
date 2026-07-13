// // lib/features/profiles/ui/viewmodels/profile_editable_viewmodel.dart
// import 'package:flutter_bloc/flutter_bloc.dart';
// import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
// import 'package:meme_inator_front/features/profiles/domain/usecases/get_my_profile_usecase.dart';
// import 'package:meme_inator_front/features/profiles/domain/usecases/patch_my_profile_usecase.dart';
// import 'package:meme_inator_front/features/profiles/domain/usecases/replace_my_profile_usecase.dart';
// import 'package:meme_inator_front/features/profiles/domain/usecases/sync_profile_media_usecase.dart';
// import 'package:meme_inator_front/features/profiles/ui/bloc/profile_states.dart';

// class ProfileEditableViewModel extends Cubit<ProfileState> {
//   final GetMyProfileUsecase getMyProfile;
//   final PatchMyProfileUsecase patchMyProfile;
//   final ReplaceMyProfileUsecase replaceMyProfile;
//   final SyncProfileMediaUsecase syncProfileMedia;

//   ProfileEntity? _currentProfile;

//   ProfileEditableViewModel({
//     required this.getMyProfile,
//     required this.patchMyProfile,
//     required this.replaceMyProfile,
//     required this.syncProfileMedia,
//   }) : super(ProfileInitial());

//   Future<void> loadMyProfile() async {
//     emit(ProfileLoading());
//     final result = await getMyProfile.execute();
//     result.match(
//       ok: (profile) {
//         _currentProfile = profile;
//         emit(ProfileLoaded(profile));
//       },
//       notOk: (notOk) => emit(ProfileError(notOk.message)),
//       error: (error) => emit(ProfileError(error.message)),
//     );
//   }

//   Future<void> updateField(String field, dynamic value) async {
//     if (_currentProfile == null) return;
    
//     // Create a copy with the updated field
//     final updated = _currentProfile!.copyWith(
//       description: field == 'description' ? value as String? : _currentProfile!.description,
//       backgroundColor: field == 'backgroundColor' ? value as String? : _currentProfile!.backgroundColor,
//       profilePicUrl: field == 'profilePicUrl' ? value as String? : _currentProfile!.profilePicUrl,
//       profileHeaderImgUrl: field == 'profileHeaderImgUrl' ? value as String? : _currentProfile!.profileHeaderImgUrl,
//       bgImg: field == 'bgImg' ? value as String? : _currentProfile!.bgImg,
//       profileThemeMusicUrl: field == 'profileThemeMusicUrl' ? value as String? : _currentProfile!.profileThemeMusicUrl,
//       isOnlineMsg: field == 'isOnlineMsg' ? value as String? : _currentProfile!.isOnlineMsg,
//       isOfflineMsg: field == 'isOfflineMsg' ? value as String? : _currentProfile!.isOfflineMsg,
//     );
    
//     _currentProfile = updated;
//     emit(ProfileLoaded(updated));
//   }

//   Future<void> saveChanges() async {
//     if (_currentProfile == null) return;
//     emit(ProfileSaving());
    
//     final result = await patchMyProfile.execute(
//       valObj: PatchMyProfileInput(
//         userId: _currentProfile!.userId, // You'll need to convert to Uuid
//         partialData: _currentProfile!.toJson(),
//       ),
//     );
    
//     result.match(
//       ok: (profile) {
//         _currentProfile = profile;
//         emit(ProfileSaved(profile));
//       },
//       notOk: (notOk) => emit(ProfileError(notOk.message)),
//       error: (error) => emit(ProfileError(error.message)),
//     );
//   }

//   Future<void> syncMedia(Map<String, dynamic> mediaPayload) async {
//     if (_currentProfile == null) return;
    
//     emit(ProfileSaving());
//     final result = await syncProfileMedia.execute(
//       valObj: SyncProfileMediaInput(
//         userId: _currentProfile!.userId, // You'll need to convert to Uuid
//         mediaPayload: mediaPayload,
//       ),
//     );
    
//     result.match(
//       ok: (profile) {
//         _currentProfile = profile;
//         emit(ProfileSaved(profile));
//       },
//       notOk: (notOk) => emit(ProfileError(notOk.message)),
//       error: (error) => emit(ProfileError(error.message)),
//     );
//   }
// }