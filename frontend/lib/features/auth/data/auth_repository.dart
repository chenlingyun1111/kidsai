import '../../../core/network/api_client.dart';
import '../../../core/storage/secure_storage.dart';

class AuthRepository {
  final _dio = ApiClient.instance.dio;

  Future<bool> register({
    required String email,
    required String password,
    required String pin,
    String? displayName,
  }) async {
    final response = await _dio.post('/auth/register', data: {
      'email': email,
      'password': password,
      'pin': pin,
      'display_name': displayName,
    });
    final token = response.data['access_token'] as String;
    await SecureStorage.saveToken(token);
    return true;
  }

  Future<bool> login({
    required String email,
    required String password,
  }) async {
    final response = await _dio.post('/auth/login', data: {
      'email': email,
      'password': password,
    });
    final token = response.data['access_token'] as String;
    await SecureStorage.saveToken(token);
    return true;
  }

  Future<bool> verifyPin(String pin) async {
    final response = await _dio.post('/auth/verify-pin', data: {'pin': pin});
    return response.data['verified'] == true;
  }

  Future<void> logout() async {
    await SecureStorage.deleteToken();
  }

  Future<bool> isLoggedIn() async {
    final token = await SecureStorage.getToken();
    return token != null;
  }
}
