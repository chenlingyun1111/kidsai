import 'package:flutter/material.dart';

class CharacterDisplay extends StatelessWidget {
  const CharacterDisplay({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: Replace with Rive animation widget
    // final riveController = StateMachineController(artboard);
    // Inputs: isListening, isTalking, emotion (happy/confused/celebrating)
    return Center(
      child: Container(
        width: 200,
        height: 200,
        decoration: BoxDecoration(
          color: const Color(0xFF6C63FF).withAlpha(50),
          shape: BoxShape.circle,
        ),
        child: const Icon(
          Icons.pets,
          size: 100,
          color: Color(0xFF6C63FF),
        ),
      ),
    );
  }
}
