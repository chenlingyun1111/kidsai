import 'dart:typed_data';
import '../../../core/network/api_client.dart';
import 'package:dio/dio.dart';

class ChatRepository {
  final _dio = ApiClient.instance.dio;

  Future<Map<String, dynamic>> sendMessage({
    required String childId,
    required String characterId,
    required String message,
  }) async {
    final response = await _dio.post('/chat', data: {
      'child_id': childId,
      'character_id': characterId,
      'message': message,
    });
    return response.data;
  }

  Future<({String text, String emotion, Uint8List audio})> sendMessageWithAudio({
    required String childId,
    required String characterId,
    required String message,
  }) async {
    final response = await _dio.post(
      '/chat/audio',
      data: {
        'child_id': childId,
        'character_id': characterId,
        'message': message,
      },
      options: Options(responseType: ResponseType.bytes),
    );

    final text = response.headers.value('x-reply-text') ?? '';
    final emotion = response.headers.value('x-character-emotion') ?? 'happy';
    final audio = Uint8List.fromList(response.data);

    return (text: text, emotion: emotion, audio: audio);
  }

  Future<void> clearSession({
    required String childId,
    required String characterId,
  }) async {
    await _dio.delete(
      '/chat/session',
      queryParameters: {
        'child_id': childId,
        'character_id': characterId,
      },
    );
  }
}
