import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/brief.dart';

class ApiService {
  ApiService({this.baseUrl = 'http://127.0.0.1:8000'});
  final String baseUrl;

  Future<ReadinessBrief> loadDemo() async {
    final response = await http.get(Uri.parse('$baseUrl/api/v1/demo'));
    if (response.statusCode != 200) {
      throw Exception('API error ${response.statusCode}: ${response.body}');
    }
    return ReadinessBrief.fromJson(jsonDecode(response.body));
  }
}
