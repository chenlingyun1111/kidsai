import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../data/character_repository.dart';
import '../../data/models/character_model.dart';
import '../../../auth/data/auth_repository.dart';

class CharacterGalleryScreen extends StatefulWidget {
  const CharacterGalleryScreen({super.key});

  @override
  State<CharacterGalleryScreen> createState() => _CharacterGalleryScreenState();
}

class _CharacterGalleryScreenState extends State<CharacterGalleryScreen> {
  final _repo = CharacterRepository();
  List<CharacterModel> _characters = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadCharacters();
  }

  Future<void> _loadCharacters() async {
    try {
      final chars = await _repo.listCharacters();
      setState(() {
        _characters = chars;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F0FF),
      appBar: AppBar(
        title: const Text('Choose your friend!'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => _showPinDialog(context),
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _characters.isEmpty
              ? _buildEmpty()
              : _buildGrid(),
    );
  }

  Widget _buildEmpty() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.pets, size: 80, color: Colors.grey[400]),
          const SizedBox(height: 16),
          Text('No characters yet!',
              style: Theme.of(context).textTheme.headlineMedium),
          const SizedBox(height: 8),
          const Text('Go to Parent Panel to create one.'),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: () => _showPinDialog(context),
            child: const Text('Open Parent Panel'),
          ),
        ],
      ),
    );
  }

  Widget _buildGrid() {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          childAspectRatio: 0.85,
        ),
        itemCount: _characters.length,
        itemBuilder: (context, index) {
          final char = _characters[index];
          return _CharacterCard(
            character: char,
            onTap: () => context.go('/chat?child_id=&character_id=${char.id}&name=${Uri.encodeComponent(char.name)}'),
          );
        },
      ),
    );
  }

  void _showPinDialog(BuildContext context) {
    final pinController = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Parent PIN'),
        content: TextField(
          controller: pinController,
          obscureText: true,
          keyboardType: TextInputType.number,
          maxLength: 4,
          decoration: const InputDecoration(hintText: 'Enter 4-digit PIN'),
          autofocus: true,
          onSubmitted: (_) => _verifyPin(ctx, pinController.text),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => _verifyPin(ctx, pinController.text),
            child: const Text('Verify'),
          ),
        ],
      ),
    );
  }

  Future<void> _verifyPin(BuildContext ctx, String pin) async {
    try {
      final verified = await AuthRepository().verifyPin(pin);
      if (verified && mounted) {
        Navigator.of(ctx).pop();
        context.go('/parent');
      }
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('Invalid PIN')));
      }
    }
  }
}

class _CharacterCard extends StatelessWidget {
  final CharacterModel character;
  final VoidCallback onTap;

  const _CharacterCard({required this.character, required this.onTap});

  IconData get _icon {
    final name = character.name.toLowerCase();
    if (name.contains('dragon') || name.contains('spark')) return Icons.whatshot;
    if (name.contains('bunny') || name.contains('luna')) return Icons.cruelty_free;
    if (name.contains('bear')) return Icons.explore;
    return Icons.pets;
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        elevation: 4,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(_icon, size: 64,
                  color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 12),
              Text(character.name,
                  style: Theme.of(context).textTheme.headlineMedium,
                  textAlign: TextAlign.center),
              const SizedBox(height: 4),
              Text(character.species,
                  style: Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(color: Colors.grey[600]),
                  textAlign: TextAlign.center),
            ],
          ),
        ),
      ),
    );
  }
}
