import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../constants/api_constants.dart';

class WebSocketManager {
  WebSocketChannel? _channel;
  final _messageController = StreamController<Map<String, dynamic>>.broadcast();
  final _audioController = StreamController<Uint8List>.broadcast();

  Stream<Map<String, dynamic>> get messages => _messageController.stream;
  Stream<Uint8List> get audioChunks => _audioController.stream;

  void connect({required String childId, required String characterId}) {
    final uri = Uri.parse(
        '${ApiConstants.wsUrl}?child_id=$childId&character_id=$characterId');
    _channel = WebSocketChannel.connect(uri);

    _channel!.stream.listen(
      (data) {
        if (data is Uint8List) {
          _audioController.add(data);
        } else if (data is String) {
          _messageController.add(jsonDecode(data));
        }
      },
      onError: (error) {
        _messageController.addError(error);
      },
      onDone: () {
        _messageController.close();
        _audioController.close();
      },
    );
  }

  void sendAudio(Uint8List audioData) {
    _channel?.sink.add(audioData);
  }

  void sendMessage(Map<String, dynamic> message) {
    _channel?.sink.add(jsonEncode(message));
  }

  void disconnect() {
    sendMessage({'type': 'session_end'});
    _channel?.sink.close();
  }

  void dispose() {
    _messageController.close();
    _audioController.close();
    _channel?.sink.close();
  }
}
