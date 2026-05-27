import '../../../core/network/api_client.dart';
import 'models/character_model.dart';

class CharacterRepository {
  final _dio = ApiClient.instance.dio;

  Future<List<CharacterModel>> listCharacters() async {
    final response = await _dio.get('/characters');
    final list = response.data as List;
    return list.map((j) => CharacterModel.fromJson(j)).toList();
  }

  Future<CharacterModel> createCharacter(Map<String, dynamic> data) async {
    final response = await _dio.post('/characters', data: data);
    return CharacterModel.fromJson(response.data);
  }

  Future<CharacterModel> updateCharacter(
      String id, Map<String, dynamic> data) async {
    final response = await _dio.put('/characters/$id', data: data);
    return CharacterModel.fromJson(response.data);
  }

  Future<void> deleteCharacter(String id) async {
    await _dio.delete('/characters/$id');
  }
}
