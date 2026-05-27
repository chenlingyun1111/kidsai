import 'package:flutter/material.dart';
import '../widgets/character_display.dart';
import '../widgets/voice_indicator.dart';

class VoiceChatScreen extends StatefulWidget {
  const VoiceChatScreen({super.key});

  @override
  State<VoiceChatScreen> createState() => _VoiceChatScreenState();
}

class _VoiceChatScreenState extends State<VoiceChatScreen> {
  bool _isListening = false;
  String _subtitle = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F0FF),
      body: SafeArea(
        child: Column(
          children: [
            // Top bar with back button and timer
            Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back_rounded, size: 32),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                  const Spacer(),
                  // Session timer
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Text('25:00',
                        style: TextStyle(fontSize: 18)),
                  ),
                ],
              ),
            ),

            // Character display area
            const Expanded(
              flex: 3,
              child: CharacterDisplay(),
            ),

            // Subtitle area
            if (_subtitle.isNotEmpty)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 32),
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white.withAlpha(200),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text(
                    _subtitle,
                    style: const TextStyle(fontSize: 18),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),

            const SizedBox(height: 16),

            // Voice input area
            Expanded(
              flex: 1,
              child: Center(
                child: GestureDetector(
                  onTapDown: (_) => _startListening(),
                  onTapUp: (_) => _stopListening(),
                  onTapCancel: () => _stopListening(),
                  child: VoiceIndicator(isActive: _isListening),
                ),
              ),
            ),

            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  void _startListening() {
    setState(() => _isListening = true);
    // TODO: start audio recording and WebSocket streaming
  }

  void _stopListening() {
    setState(() => _isListening = false);
    // TODO: stop recording, send final audio chunk
  }
}
