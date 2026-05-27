import 'package:flutter/material.dart';
import '../bloc/voice_chat_state.dart';

class CharacterDisplay extends StatelessWidget {
  final String emotion;
  final ChatStatus status;

  const CharacterDisplay({
    super.key,
    this.emotion = 'idle',
    this.status = ChatStatus.idle,
  });

  Color get _glowColor {
    switch (status) {
      case ChatStatus.speaking:
        return const Color(0xFF6C63FF);
      case ChatStatus.thinking:
        return Colors.amber;
      case ChatStatus.listening:
        return Colors.green;
      case ChatStatus.idle:
        return Colors.transparent;
    }
  }

  IconData get _emotionIcon {
    switch (emotion) {
      case 'happy':
        return Icons.sentiment_very_satisfied;
      case 'confused':
        return Icons.sentiment_neutral;
      case 'celebrating':
        return Icons.celebration;
      default:
        return Icons.pets;
    }
  }

  @override
  Widget build(BuildContext context) {
    // TODO: Replace with Rive animation
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Center(
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          width: 160,
          height: 160,
          decoration: BoxDecoration(
            color: const Color(0xFF6C63FF).withAlpha(30),
            shape: BoxShape.circle,
            boxShadow: status != ChatStatus.idle
                ? [
                    BoxShadow(
                      color: _glowColor.withAlpha(80),
                      blurRadius: 30,
                      spreadRadius: 10,
                    )
                  ]
                : [],
          ),
          child: Icon(_emotionIcon, size: 80, color: const Color(0xFF6C63FF)),
        ),
      ),
    );
  }
}
