enum ChatStatus { idle, listening, thinking, speaking }

class VoiceChatState {
  final ChatStatus status;
  final List<ChatMessage> messages;
  final String? currentSubtitle;
  final String characterEmotion;
  final int remainingSeconds;

  const VoiceChatState({
    this.status = ChatStatus.idle,
    this.messages = const [],
    this.currentSubtitle,
    this.characterEmotion = 'idle',
    this.remainingSeconds = 1800,
  });

  VoiceChatState copyWith({
    ChatStatus? status,
    List<ChatMessage>? messages,
    String? currentSubtitle,
    String? characterEmotion,
    int? remainingSeconds,
  }) =>
      VoiceChatState(
        status: status ?? this.status,
        messages: messages ?? this.messages,
        currentSubtitle: currentSubtitle ?? this.currentSubtitle,
        characterEmotion: characterEmotion ?? this.characterEmotion,
        remainingSeconds: remainingSeconds ?? this.remainingSeconds,
      );
}

class ChatMessage {
  final String role; // 'child' or 'character'
  final String text;
  final DateTime timestamp;

  ChatMessage({
    required this.role,
    required this.text,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();
}
