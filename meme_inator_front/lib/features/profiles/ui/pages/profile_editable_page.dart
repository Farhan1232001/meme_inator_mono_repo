// // lib/features/profiles/ui/pages/profile_editable_page.dart
// import 'package:flutter/material.dart';
// import 'package:flutter_bloc/flutter_bloc.dart';
// import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';
// import 'package:meme_inator_front/features/profiles/ui/bloc/profile_states.dart';
// import 'package:meme_inator_front/features/profiles/ui/viewmodels/profile_editable_viewmodel.dart';

// class ProfileEditablePage extends StatefulWidget {
//   const ProfileEditablePage({Key? key}) : super(key: key);

//   @override
//   State<ProfileEditablePage> createState() => _ProfileEditablePageState();
// }

// class _ProfileEditablePageState extends State<ProfileEditablePage> {
//   final _formKey = GlobalKey<FormState>();
//   late TextEditingController _descriptionController;

//   @override
//   void initState() {
//     super.initState();
//     _descriptionController = TextEditingController();
//     context.read<ProfileEditableViewModel>().loadMyProfile();
//   }

//   @override
//   void dispose() {
//     _descriptionController.dispose();
//     super.dispose();
//   }

//   @override
//   Widget build(BuildContext context) {
//     return PlatformScaffold(
//       appBar: PlatformAppBar(
//         title: const Text('Edit Profile'),
//         actions: [
//           PlatformTextButton(
//             onPressed: _save,
//             child: const Text('Save'),
//           ),
//         ],
//       ),
//       body: BlocConsumer<ProfileEditableViewModel, ProfileState>(
//         listener: (context, state) {
//           if (state is ProfileSaved) {
//             Navigator.pop(context);
//           } else if (state is ProfileError) {
//             _showError(context, state.message);
//           }
//         },
//         builder: (context, state) {
//           if (state is ProfileLoading) {
//             return const Center(child: PlatformCircularProgressIndicator());
//           } else if (state is ProfileLoaded) {
//             final profile = state.profile;
//             _descriptionController.text = profile.description ?? '';
//             return Padding(
//               padding: const EdgeInsets.all(16),
//               child: Form(
//                 key: _formKey,
//                 child: ListView(
//                   children: [
//                     // Profile picture (tap to change)
//                     Center(
//                       child: GestureDetector(
//                         onTap: () => _pickImage('profile'),
//                         child: CircleAvatar(
//                           radius: 50,
//                           backgroundImage: profile.profilePicUrl != null
//                               ? NetworkImage(profile.profilePicUrl!)
//                               : null,
//                           child: profile.profilePicUrl == null
//                               ? const Icon(Icons.camera_alt, size: 40)
//                               : null,
//                         ),
//                       ),
//                     ),
//                     const SizedBox(height: 16),
//                     // Description
//                     PlatformTextFormField(
//                       controller: _descriptionController,
//                       hintText: 'Description',
//                       maxLines: 3,
//                       onChanged: (value) {
//                         context.read<ProfileEditableViewModel>().updateField('description', value);
//                       },
//                     ),
//                     // Add other fields as needed
//                   ],
//                 ),
//               ),
//             );
//           } else if (state is ProfileSaving) {
//             return const Center(child: PlatformCircularProgressIndicator());
//           }
//           return const SizedBox.shrink();
//         },
//       ),
//     );
//   }

//   void _save() {
//     if (_formKey.currentState?.validate() ?? false) {
//       context.read<ProfileEditableViewModel>().saveChanges();
//     }
//   }

//   void _pickImage(String type) {
//     // Implement image picker, upload, then call syncMedia
//     // You'll need to implement this based on your image picker solution
//     showPlatformDialog(
//       context: context,
//       builder: (_) => PlatformAlertDialog(
//         title: const Text('Coming Soon'),
//         content: const Text('Image picking will be implemented soon.'),
//         actions: [
//           PlatformDialogAction(
//             child: const Text('OK'),
//             onPressed: () => Navigator.pop(context),
//           ),
//         ],
//       ),
//     );
//   }

//   void _showError(BuildContext context, String message) {
//     showPlatformDialog(
//       context: context,
//       builder: (_) => PlatformAlertDialog(
//         title: const Text('Error'),
//         content: Text(message),
//         actions: [
//           PlatformDialogAction(
//             child: const Text('OK'),
//             onPressed: () => Navigator.pop(context),
//           ),
//         ],
//       ),
//     );
//   }
// }