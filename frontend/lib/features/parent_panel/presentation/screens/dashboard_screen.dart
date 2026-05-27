import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../characters/data/character_repository.dart';
import '../../../characters/data/models/character_model.dart';
import '../../../../core/network/api_client.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          leading: IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () => context.go('/characters'),
          ),
          title: const Text('Parent Panel'),
          bottom: const TabBar(
            isScrollable: true,
            tabs: [
              Tab(icon: Icon(Icons.dashboard), text: 'Overview'),
              Tab(icon: Icon(Icons.book), text: 'Courseware'),
              Tab(icon: Icon(Icons.face), text: 'Characters'),
              Tab(icon: Icon(Icons.settings), text: 'Settings'),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            _OverviewTab(),
            _CoursewareTab(),
            _CharactersTab(),
            _SettingsTab(),
          ],
        ),
      ),
    );
  }
}

class _OverviewTab extends StatefulWidget {
  const _OverviewTab();

  @override
  State<_OverviewTab> createState() => _OverviewTabState();
}

class _OverviewTabState extends State<_OverviewTab> {
  List<dynamic> _conversations = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final resp = await ApiClient.instance.dio.get('/conversations');
      setState(() => _conversations = resp.data as List);
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Recent Conversations',
                    style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 16),
                if (_conversations.isEmpty)
                  const Text('No conversations yet. Let your child chat with a character!')
                else
                  ...(_conversations.take(10).map((c) => ListTile(
                        leading: const Icon(Icons.chat_bubble_outline),
                        title: Text('${c['turn_count'] ?? 0} turns'),
                        subtitle: Text(c['summary'] ?? 'No summary'),
                      ))),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _CoursewareTab extends StatelessWidget {
  const _CoursewareTab();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          ElevatedButton.icon(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('File upload coming in Phase 2')),
              );
            },
            icon: const Icon(Icons.upload_file),
            label: const Text('Upload Courseware'),
          ),
          const SizedBox(height: 24),
          const Expanded(
            child: Center(
              child: Text('Upload your child\'s English learning materials here.\n'
                  'Supported: PDF, images, text files.',
                  textAlign: TextAlign.center),
            ),
          ),
        ],
      ),
    );
  }
}

class _CharactersTab extends StatefulWidget {
  const _CharactersTab();

  @override
  State<_CharactersTab> createState() => _CharactersTabState();
}

class _CharactersTabState extends State<_CharactersTab> {
  final _repo = CharacterRepository();
  List<CharacterModel> _characters = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final chars = await _repo.listCharacters();
      setState(() {
        _characters = chars;
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Center(child: CircularProgressIndicator());

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          ElevatedButton.icon(
            onPressed: () => _showCreateDialog(context),
            icon: const Icon(Icons.add),
            label: const Text('Create Character'),
          ),
          const SizedBox(height: 16),
          Expanded(
            child: ListView.builder(
              itemCount: _characters.length,
              itemBuilder: (context, i) {
                final c = _characters[i];
                return Card(
                  child: ListTile(
                    leading: const Icon(Icons.pets, color: Colors.deepPurple),
                    title: Text(c.name),
                    subtitle: Text(c.species.isNotEmpty ? c.species : c.personality),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete_outline),
                      onPressed: () async {
                        await _repo.deleteCharacter(c.id);
                        _load();
                      },
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  void _showCreateDialog(BuildContext context) {
    final nameCtrl = TextEditingController();
    final speciesCtrl = TextEditingController();
    final personalityCtrl = TextEditingController();
    final styleCtrl = TextEditingController();

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Create Character'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameCtrl,
                decoration: const InputDecoration(labelText: 'Name'),
              ),
              TextField(
                controller: speciesCtrl,
                decoration: const InputDecoration(labelText: 'Species (e.g., Baby Dragon)'),
              ),
              TextField(
                controller: personalityCtrl,
                decoration: const InputDecoration(labelText: 'Personality'),
              ),
              TextField(
                controller: styleCtrl,
                decoration: const InputDecoration(labelText: 'Speaking style'),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              await _repo.createCharacter({
                'name': nameCtrl.text,
                'personality': personalityCtrl.text,
                'speaking_style': styleCtrl.text.isEmpty ? 'Short and simple' : styleCtrl.text,
                'world_rules': {
                  'character_meta': {
                    'name': nameCtrl.text,
                    'species': speciesCtrl.text,
                    'world': 'A magical world',
                  },
                  'personality': {
                    'traits': personalityCtrl.text.split(',').map((s) => s.trim()).toList(),
                  },
                  'speaking_style': {
                    'vocabulary_level': 'simple, age-appropriate',
                    'sentence_length': '5-10 words',
                  },
                  'teaching_behavior': {
                    'correction_style': 'gentle_redirect',
                    'singing_enabled': true,
                    'game_types': ['rhyming', 'word_chain'],
                  },
                  'safety_rules': {
                    'never_discuss': ['violence', 'scary topics'],
                    'redirect_to': 'Let\'s talk about something fun!',
                  },
                },
              });
              if (ctx.mounted) Navigator.of(ctx).pop();
              _load();
            },
            child: const Text('Create'),
          ),
        ],
      ),
    );
  }
}

class _SettingsTab extends StatefulWidget {
  const _SettingsTab();

  @override
  State<_SettingsTab> createState() => _SettingsTabState();
}

class _SettingsTabState extends State<_SettingsTab> {
  final _notesController = TextEditingController();
  bool _singingEnabled = true;
  bool _gamesEnabled = true;

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('AI Behavior',
                    style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 16),
                SwitchListTile(
                  title: const Text('Singing Mode'),
                  subtitle: const Text('Allow character to sing songs'),
                  value: _singingEnabled,
                  onChanged: (v) => setState(() => _singingEnabled = v),
                ),
                SwitchListTile(
                  title: const Text('Game Mode'),
                  subtitle: const Text('Include word games in conversation'),
                  value: _gamesEnabled,
                  onChanged: (v) => setState(() => _gamesEnabled = v),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Notes for AI',
                    style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 8),
                const Text('These notes will guide the AI in the next session'),
                const SizedBox(height: 16),
                TextField(
                  controller: _notesController,
                  maxLines: 4,
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'e.g., Focus on animal words today...',
                  ),
                ),
                const SizedBox(height: 8),
                ElevatedButton(
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Settings saved')),
                    );
                  },
                  child: const Text('Save'),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  @override
  void dispose() {
    _notesController.dispose();
    super.dispose();
  }
}
