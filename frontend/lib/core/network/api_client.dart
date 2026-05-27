import 'package:dio/dio.dart';
import '../constants/api_constants.dart';
import '../storage/secure_storage.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._();
  static ApiClient get instance => _instance;

  late final Dio dio;

  ApiClient._() {
    dio = Dio(BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      headers: {'Content-Type': 'application/json'},
    ));

    dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await SecureStorage.getToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) {
        if (error.response?.statusCode == 401) {
          SecureStorage.deleteToken();
        }
        handler.next(error);
      },
    ));
  }
}
