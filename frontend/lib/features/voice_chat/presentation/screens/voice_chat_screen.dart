import 'package:flutter/material.dart';
import '../bloc/voice_chat_bloc.dart';
import '../bloc/voice_chat_state.dart';
import '../widgets/character_display.dart';

class VoiceChatScreen extends StatefulWidget {
  final String? childId;
  final String? characterId;
  final String? characterName;

  const VoiceChatScreen({
    super.key,
    this.childId,
    this.characterId,
    this.characterName,
  });

  @override
  State<VoiceChatScreen> createState() => _VoiceChatScreenState();
}

class _VoiceChatScreenState extends State<VoiceChatScreen> {
  late final VoiceChatBloc _bloc;
  final _textController = TextEditingController();
  final _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _bloc = VoiceChatBloc(
      childId: widget.childId ?? '',
      characterId: widget.characterId ?? '',
      characterName: widget.characterName ?? 'Spark',
    );
    _bloc.addListener(_onStateChange);
    _bloc.connect();
  }

  void _onStateChange() {
    setState(() {});
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = _bloc.state;
    final minutes = state.remainingSeconds ~/ 60;
    final seconds = state.remainingSeconds % 60;

    return Scaffold(
      backgroundColor: const Color(0xFFF5F0FF),
      body: SafeArea(
        child: Column(
          children: [
            // Top bar
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back_rounded, size: 28),
                    onPressed: () {
                      _bloc.disconnect();
                      Navigator.of(context).pop();
                    },
                  ),
                  Text(widget.characterName ?? 'Spark',
                      style: Theme.of(context).textTheme.headlineMedium),
                  const Spacer(),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: state.remainingSeconds < 300
                          ? Colors.red[100]
                          : Colors.white,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Text(
                      '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}',
                      style: TextStyle(
                        fontSize: 16,
                        color: state.remainingSeconds < 300
                            ? Colors.red
                            : Colors.black87,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // Character display
            CharacterDisplay(
              emotion: state.characterEmotion,
              status: state.status,
            ),

            // Subtitle
            if (state.currentSubtitle != null &&
                state.currentSubtitle!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.white.withAlpha(220),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text(
                    state.currentSubtitle!,
                    style: const TextStyle(fontSize: 16),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),

            const SizedBox(height: 8),

            // Chat history
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: state.messages.length,
                itemBuilder: (context, index) {
                  final msg = state.messages[index];
                  final isChild = msg.role == 'child';
                  return Align(
                    alignment:
                        isChild ? Alignment.centerRight : Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 10),
                      constraints: BoxConstraints(
                          maxWidth: MediaQuery.of(context).size.width * 0.75),
                      decoration: BoxDecoration(
                        color: isChild
                            ? Theme.of(context).colorScheme.primary
                            : Colors.white,
                        borderRadius: BorderRadius.circular(18),
                      ),
                      child: Text(
                        msg.text,
                        style: TextStyle(
                          fontSize: 16,
                          color: isChild ? Colors.white : Colors.black87,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),

            // Status indicator
            if (state.status == ChatStatus.thinking)
              const Padding(
                padding: EdgeInsets.all(8),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2)),
                    SizedBox(width: 8),
                    Text('Thinking...'),
                  ],
                ),
              ),

            // Text input
            Container(
              padding: const EdgeInsets.all(12),
              decoration: const BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(color: Colors.black12, blurRadius: 4, offset: Offset(0, -2))
                ],
              ),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _textController,
                      decoration: InputDecoration(
                        hintText: 'Type a message...',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: BorderSide.none,
                        ),
                        filled: true,
                        fillColor: const Color(0xFFF5F0FF),
                        contentPadding: const EdgeInsets.symmetric(
                            horizontal: 20, vertical: 12),
                      ),
                      textInputAction: TextInputAction.send,
                      onSubmitted: _sendMessage,
                    ),
                  ),
                  const SizedBox(width: 8),
                  FloatingActionButton(
                    mini: true,
                    onPressed: () => _sendMessage(_textController.text),
                    child: const Icon(Icons.send),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _sendMessage(String text) {
    if (text.trim().isEmpty) return;
    _bloc.sendTextMessage(text.trim());
    _textController.clear();
  }

  @override
  void dispose() {
    _bloc.removeListener(_onStateChange);
    _bloc.dispose();
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }
}
