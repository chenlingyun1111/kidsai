import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import '../../../../core/constants/api_constants.dart';
import 'voice_chat_state.dart';

class VoiceChatBloc extends ChangeNotifier {
  final String childId;
  final String characterId;
  final String characterName;

  VoiceChatState _state = const VoiceChatState();
  VoiceChatState get state => _state;

  WebSocketChannel? _channel;
  final AudioPlayer _audioPlayer = AudioPlayer();
  final List<int> _audioBuffer = [];
  Timer? _timer;

  VoiceChatBloc({
    required this.childId,
    required this.characterId,
    this.characterName = 'Spark',
  });

  void connect() {
    final uri = Uri.parse(
        '${ApiConstants.wsUrl}?child_id=$childId&character_id=$characterId');
    _channel = WebSocketChannel.connect(uri);

    _channel!.stream.listen(
      _onMessage,
      onError: (e) => _updateState(status: ChatStatus.idle),
      onDone: () => _updateState(status: ChatStatus.idle),
    );

    _startTimer();
  }

  void _onMessage(dynamic data) {
    if (data is List<int>) {
      _audioBuffer.addAll(data);
    } else if (data is String) {
      final msg = jsonDecode(data) as Map<String, dynamic>;
      switch (msg['type']) {
        case 'ai_text':
          final text = msg['text'] as String;
          _addMessage('character', text);
          _updateState(
            status: ChatStatus.speaking,
            currentSubtitle: text,
            characterEmotion: msg['character_emotion'] ?? 'happy',
          );
        case 'ai_text_partial':
          final partial = msg['text'] as String;
          _updateState(
            status: ChatStatus.speaking,
            currentSubtitle: (_state.currentSubtitle ?? '') + partial,
          );
        case 'ai_turn_complete':
          _playBufferedAudio();
          _updateState(
            status: ChatStatus.idle,
            characterEmotion: msg['character_emotion'] ?? 'idle',
          );
        case 'transcript_final':
          _addMessage('child', msg['text'] as String);
      }
    }
  }

  void sendTextMessage(String text) {
    if (text.trim().isEmpty) return;

    _addMessage('child', text);
    _updateState(status: ChatStatus.thinking, currentSubtitle: null);
    _audioBuffer.clear();

    _channel?.sink.add(jsonEncode({
      'type': 'text_message',
      'text': text,
    }));
  }

  void interrupt() {
    _channel?.sink.add(jsonEncode({'type': 'interrupt'}));
    _audioPlayer.stop();
    _audioBuffer.clear();
    _updateState(status: ChatStatus.idle);
  }

  Future<void> _playBufferedAudio() async {
    if (_audioBuffer.isEmpty) return;

    try {
      final dir = await getTemporaryDirectory();
      final file = File('${dir.path}/reply_${DateTime.now().millisecondsSinceEpoch}.mp3');
      await file.writeAsBytes(Uint8List.fromList(_audioBuffer));
      _audioBuffer.clear();

      await _audioPlayer.play(DeviceFileSource(file.path));
      _audioPlayer.onPlayerComplete.listen((_) {
        _updateState(characterEmotion: 'idle');
      });
    } catch (_) {
      _audioBuffer.clear();
    }
  }

  void _addMessage(String role, String text) {
    final updated = List<ChatMessage>.from(_state.messages)
      ..add(ChatMessage(role: role, text: text));
    _updateState(messages: updated);
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (_state.remainingSeconds > 0) {
        _updateState(remainingSeconds: _state.remainingSeconds - 1);
      }
    });
  }

  void _updateState({
    ChatStatus? status,
    List<ChatMessage>? messages,
    String? currentSubtitle,
    String? characterEmotion,
    int? remainingSeconds,
  }) {
    _state = _state.copyWith(
      status: status,
      messages: messages,
      currentSubtitle: currentSubtitle,
      characterEmotion: characterEmotion,
      remainingSeconds: remainingSeconds,
    );
    notifyListeners();
  }

  void disconnect() {
    _channel?.sink.add(jsonEncode({'type': 'session_end'}));
    _channel?.sink.close();
    _timer?.cancel();
    _audioPlayer.dispose();
  }

  @override
  void dispose() {
    disconnect();
    super.dispose();
  }
}
