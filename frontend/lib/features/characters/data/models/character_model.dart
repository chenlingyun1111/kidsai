class CharacterModel {
  final String id;
  final String name;
  final String? description;
  final String personality;
  final String? backstory;
  final String speakingStyle;
  final List<String> catchphrases;
  final String? voiceId;
  final String? riveAssetUrl;
  final Map<String, dynamic> worldRules;
  final bool isActive;

  CharacterModel({
    required this.id,
    required this.name,
    this.description,
    required this.personality,
    this.backstory,
    required this.speakingStyle,
    this.catchphrases = const [],
    this.voiceId,
    this.riveAssetUrl,
    this.worldRules = const {},
    this.isActive = true,
  });

  factory CharacterModel.fromJson(Map<String, dynamic> json) => CharacterModel(
        id: json['id'],
        name: json['name'],
        description: json['description'],
        personality: json['personality'],
        backstory: json['backstory'],
        speakingStyle: json['speaking_style'],
        catchphrases: List<String>.from(json['catchphrases'] ?? []),
        voiceId: json['voice_id'],
        riveAssetUrl: json['rive_asset_url'],
        worldRules: Map<String, dynamic>.from(json['world_rules'] ?? {}),
        isActive: json['is_active'] ?? true,
      );

  String get species =>
      (worldRules['character_meta'] as Map?)?['species'] ?? '';
}
