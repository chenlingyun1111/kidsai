class ChildModel {
  final String id;
  final String displayName;
  final int? age;
  final String englishLevel;
  final int dailyTimeLimitMinutes;

  ChildModel({
    required this.id,
    required this.displayName,
    this.age,
    this.englishLevel = 'beginner',
    this.dailyTimeLimitMinutes = 30,
  });

  factory ChildModel.fromJson(Map<String, dynamic> json) => ChildModel(
        id: json['id'],
        displayName: json['display_name'],
        age: json['age'],
        englishLevel: json['english_level'] ?? 'beginner',
        dailyTimeLimitMinutes: json['daily_time_limit_minutes'] ?? 30,
      );
}
