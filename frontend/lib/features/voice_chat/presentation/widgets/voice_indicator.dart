import 'package:flutter/material.dart';

class VoiceIndicator extends StatelessWidget {
  final bool isActive;

  const VoiceIndicator({super.key, required this.isActive});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      width: isActive ? 100 : 80,
      height: isActive ? 100 : 80,
      decoration: BoxDecoration(
        color: isActive
            ? Theme.of(context).colorScheme.primary
            : Theme.of(context).colorScheme.primary.withAlpha(150),
        shape: BoxShape.circle,
        boxShadow: isActive
            ? [
                BoxShadow(
                  color: Theme.of(context).colorScheme.primary.withAlpha(100),
                  blurRadius: 30,
                  spreadRadius: 10,
                )
              ]
            : [],
      ),
      child: Icon(
        isActive ? Icons.mic : Icons.mic_none,
        color: Colors.white,
        size: 40,
      ),
    );
  }
}
