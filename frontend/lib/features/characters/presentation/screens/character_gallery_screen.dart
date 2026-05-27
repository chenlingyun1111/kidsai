import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class CharacterGalleryScreen extends StatelessWidget {
  const CharacterGalleryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: fetch characters from API
    final characters = [
      {'name': 'Spark', 'description': 'Baby Dragon', 'icon': Icons.whatshot},
      {'name': 'Luna', 'description': 'Magic Bunny', 'icon': Icons.cruelty_free},
      {'name': 'Captain Bear', 'description': 'Explorer Bear', 'icon': Icons.explore},
    ];

    return Scaffold(
      backgroundColor: const Color(0xFFF5F0FF),
      appBar: AppBar(
        title: const Text('Choose your friend!'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          // Parent panel access (PIN protected)
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => _showPinDialog(context),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            childAspectRatio: 0.85,
          ),
          itemCount: characters.length,
          itemBuilder: (context, index) {
            final char = characters[index];
            return _CharacterCard(
              name: char['name'] as String,
              description: char['description'] as String,
              icon: char['icon'] as IconData,
              onTap: () => context.go('/chat'),
            );
          },
        ),
      ),
    );
  }

  void _showPinDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Parent PIN'),
        content: TextField(
          obscureText: true,
          keyboardType: TextInputType.number,
          maxLength: 4,
          decoration: const InputDecoration(hintText: 'Enter 4-digit PIN'),
          onSubmitted: (pin) {
            // TODO: verify PIN via API
            Navigator.of(ctx).pop();
            context.go('/parent');
          },
        ),
      ),
    );
  }
}

class _CharacterCard extends StatelessWidget {
  final String name;
  final String description;
  final IconData icon;
  final VoidCallback onTap;

  const _CharacterCard({
    required this.name,
    required this.description,
    required this.icon,
    required this.onTap,
  });

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
              Icon(icon, size: 64, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 12),
              Text(name, style: Theme.of(context).textTheme.headlineMedium),
              const SizedBox(height: 4),
              Text(description,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Colors.grey[600],
                      )),
            ],
          ),
        ),
      ),
    );
  }
}
