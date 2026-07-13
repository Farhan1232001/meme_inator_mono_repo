import 'package:equatable/equatable.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';

abstract class ProfileState extends Equatable {
  const ProfileState();
  @override
  List<Object?> get props => [];
}

class ProfileInitial extends ProfileState {}

class ProfileLoading extends ProfileState {}

class ProfileLoaded extends ProfileState {
  final ProfileEntity profile;
  final bool isAudioLoading;
  final String? audioError;

  const ProfileLoaded(
    this.profile, 
    this.isAudioLoading, 
    {this.audioError}
  );

  bool get isAudioReady => !isAudioLoading;
  bool get hasAudioError => audioError != null;

  @override
  List<Object?> get props => [profile, isAudioLoading, audioError];
}
class ProfileError extends ProfileState {
  final String message;
  const ProfileError(this.message);
  @override
  List<Object?> get props => [message];
}

// For editable profile
class ProfileSaving extends ProfileState {}
// should this extend ProfileLoaded or ProfileState??? 
class ProfileSaved extends ProfileLoaded  {
  const ProfileSaved(ProfileEntity profile) : super(profile, false);
}
