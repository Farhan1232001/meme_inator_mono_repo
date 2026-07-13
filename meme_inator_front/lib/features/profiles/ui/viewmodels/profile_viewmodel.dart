// lib/features/profiles/ui/viewmodels/profile_viewmodel.dart
import 'dart:async';

import 'package:audio_session/audio_session.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meme_inator_front/core/audio/safe_audio_player.dart';
import 'package:meme_inator_front/features/feeds/ui/config/feed_config.dart';
import 'package:meme_inator_front/features/feeds/ui/viewmodels/feed_viewmodel.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/profile_entity.dart';
import 'package:meme_inator_front/features/profiles/domain/entities/vos/get_public_profile_request_vo.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_profile_posts_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_public_profile_usecase.dart';
import 'package:meme_inator_front/features/profiles/domain/usecases/get_public_profile_with_followship_uc.dart';
import 'package:meme_inator_front/features/profiles/ui/bloc/profile_states.dart';
import 'package:meme_inator_front/features/profiles/ui/controllers/profile_feed_controller.dart';

class ProfileViewModel extends Cubit<ProfileState> {
  // Dependencies
  final GetPublicProfileUsecase getPublicProfile;
  final GetPublicProfileWithFollowshipUsecase getPublicProfileWithFollowship;
  final GetProfilePostsUsecase getProfilePosts;
  final ProfileFeedController _profileFeedController;

  // Audio player
  late final SafeAudioPlayer _audioPlayer;

  // State (maybe better to move these in ProfileLoaded state)
  late String _currentUserId;
  late String _currentUsername;
  final String? viewerUserId;
  late FeedType _currentFeedType;
  ProfileEntity? _currentProfile;

  // Public getters
  FeedViewModel get feedViewModel =>
      _profileFeedController.currentFeedViewModel!;

  SafeAudioPlayer get audioPlayer => _audioPlayer;
  ProfileEntity? get currentProfile => _currentProfile;

  // ============================================================================
  // Constructor & Lifecycle
  // ============================================================================

  ProfileViewModel({
    required this.getPublicProfile,
    required this.getPublicProfileWithFollowship,
    required this.getProfilePosts,
    this.viewerUserId,
    ProfileFeedController? feedController,
  }) : _profileFeedController = feedController ?? ProfileFeedController(),
       super(ProfileInitial()) {
    _initializeAudioPlayer();
  }

  @override
  Future<void> close() async {
    await _disposeAudio();
    await _profileFeedController.dispose();
    await super.close();
  }

  // ============================================================================
  // Profile Loading
  // ============================================================================

  Future<void> loadProfile(String username, FeedType type) async {
    _currentUsername = username;
    _currentFeedType = type;
    emit(ProfileLoading());

    final request = GetPublicProfileRequestVo(username: username, viewerUserId: viewerUserId, );
    final profileResult = await getPublicProfile.execute(request: request);

    final finalResult = profileResult.match(
      ok: (profile) {
        _currentProfile = profile as ProfileEntity;
        unawaited(_loadProfileFeed(username, type));
        unawaited(_setProfileMusic());
        return ProfileLoaded(
          _currentProfile!,
          true,
        ); // Start with audio loading
      },
      notOk: (notOk) => ProfileError(notOk.message),
      error: (error) => ProfileError(error.message),
    );

    // Now emit the result
    emit(finalResult);
  }

    Future<void> loadProfileWithFollowshipContext(String userId, FeedType type) async {
    _currentUserId = userId;
    _currentFeedType = type;
    emit(ProfileLoading());

    final profileResult = await getPublicProfileWithFollowship.execute(
      profileOwnerUserId: _currentUserId,
      viewerUserId: null,
      fields: null
    );

    final finalResult = profileResult.match(
      ok: (profile) {
        _currentProfile = profile as ProfileEntity;
        _currentUsername = profile.username;
        unawaited(_loadProfileFeed(_currentUsername, type));
        unawaited(_setProfileMusic());
        return ProfileLoaded(
          _currentProfile!,
          true,
        ); // Start with audio loading
      },
      notOk: (notOk) => ProfileError(notOk.message),
      error: (error) => ProfileError(error.message),
    );

    // Now emit the result
    emit(finalResult);
  }

  Future<void> _loadProfileFeed(String username, FeedType type) async {
    try {
      await _profileFeedController.getOrInitProfileFeed(username, type);
    } catch (e) {
      debugPrint('Feed init error: $e');
      emit(const ProfileError('Failed to initialize feed'));
    }
  }

  // ============================================================================
  // Feed Management
  // ============================================================================

  void refreshAllProfile() {
    unawaited(loadProfileWithFollowshipContext(_currentUserId, _currentFeedType));
    unawaited(refreshAudioPlayer());
    unawaited(_profileFeedController.refreshFeed());
  }

  void clearFeedRepository() {
    _profileFeedController.clearFeedRepository();
  }

  void clearProfile() {
    emit(ProfileInitial());
  }

  void updateProfile(ProfileEntity updatedProfile) {
    _currentProfile = updatedProfile;
    if (state is ProfileLoaded) {
      emit(
        ProfileLoaded(updatedProfile, (state as ProfileLoaded).isAudioLoading),
      );
    }
  }

  // ============================================================================
  // Audio Management
  // ============================================================================

  Future<void> _initializeAudioPlayer() async {
    _audioPlayer = SafeAudioPlayer();
    await _configureAudioSession();
  }

  Future<void> refreshAudioPlayer() async {
    await _setProfileMusic();
  }

  Future<void> _configureAudioSession() async {
    try {
      final session = await AudioSession.instance;
      await session.configure(const AudioSessionConfiguration.music());
      debugPrint('Audio session configured successfully');
    } catch (e) {
      debugPrint('Failed to configure audio session: $e');
    }
  }

  Future<void> _setProfileMusic() async {
    if (_currentProfile == null) {
      debugPrint('No profile loaded, cannot play music');
      return;
    }

    // final musicUrl = _currentProfile!.profileThemeMusicUrl;
    final musicUrl =
        'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3';

    // If no music URL, just mark audio as loaded (nothing to play)
    if (musicUrl == null || musicUrl.isEmpty) {
      debugPrint('No music URL provided for this profile');
      if (_currentProfile != null && state is ProfileLoaded) {
        emit(
          ProfileLoaded(
            _currentProfile!,
            false, // Audio loading complete
            audioError: null, // No error, just no music
          ),
        );
      }
      return;
    }

    await _setAudioSource(musicUrl);
  }

  Future<void> _setAudioSource(String url) async {
    if (url.isEmpty) return;

    try {
      await _audioPlayer.stop();
      await _audioPlayer.setSource(Uri.parse(url), loop: true);
      await _audioPlayer.play();

      // Audio is now ready – update state with success
      if (_currentProfile != null && state is ProfileLoaded) {
        emit(
          ProfileLoaded(
            _currentProfile!,
            false, // Audio loading complete
            audioError: null, // Clear any previous errors
          ),
        );
      }
    } catch (e) {
      debugPrint('Failed to set audio source: $e');

      // Emit error state
      if (_currentProfile != null && state is ProfileLoaded) {
        emit(
          ProfileLoaded(
            _currentProfile!,
            false, // Loading is complete (failed)
            audioError: 'Failed to load audio: ${e.toString()}',
          ),
        );
      }
    }
  }

  Future<void> _disposeAudio() async {
    await _audioPlayer.dispose();
    debugPrint('Audio player disposed');
  }

  // ============================================================================
  // Public Audio Controls (Optional)
  // ============================================================================

  Future<void> playMusic() async {
    await _setProfileMusic();
  }

  Future<void> pauseMusic() async {
    await _audioPlayer.pause();
  }

  Future<void> stopMusic() async {
    await _audioPlayer.stop();
  }

  bool get isMusicPlaying => _audioPlayer.rawPlayer.playing;

  // Method to retry audio if it failed
  Future<void> retryAudio() async {
    if (_currentProfile != null) {
      // Set loading state
      if (state is ProfileLoaded) {
        final currentState = state as ProfileLoaded;
        emit(
          ProfileLoaded(
            currentState.profile,
            true, // Loading again
            audioError: null,
          ),
        );
      }
      // Retry loading audio
      await _setProfileMusic();
    }
  }
}
