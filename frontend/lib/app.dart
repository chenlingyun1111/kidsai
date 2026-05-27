import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'features/voice_chat/presentation/screens/voice_chat_screen.dart';
import 'features/characters/presentation/screens/character_gallery_screen.dart';
import 'features/parent_panel/presentation/screens/dashboard_screen.dart';
import 'features/auth/presentation/screens/login_screen.dart';
import 'shared/theme/child_theme.dart';

class KidsAIApp extends StatelessWidget {
  const KidsAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'KidsAI',
      theme: childTheme,
      routerConfig: _router,
      debugShowCheckedModeBanner: false,
    );
  }
}

final _router = GoRouter(
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/chat',
      builder: (context, state) => const VoiceChatScreen(),
    ),
    GoRoute(
      path: '/characters',
      builder: (context, state) => const CharacterGalleryScreen(),
    ),
    GoRoute(
      path: '/parent',
      builder: (context, state) => const DashboardScreen(),
    ),
  ],
);
