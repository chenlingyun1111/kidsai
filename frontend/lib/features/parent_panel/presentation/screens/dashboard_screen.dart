import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
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
        body: TabBarView(
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

class _OverviewTab extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Learning progress summary
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Learning Progress',
                    style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 16),
                // TODO: progress charts from API data
                const LinearProgressIndicator(value: 0.6),
                const SizedBox(height: 8),
                const Text('Vocabulary: 45/75 words mastered'),
                const SizedBox(height: 16),
                const LinearProgressIndicator(value: 0.3),
                const SizedBox(height: 8),
                const Text('Phrases: 12/40 practiced'),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Recent conversations
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Recent Conversations',
                    style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 16),
                // TODO: fetch from API
                const ListTile(
                  leading: Icon(Icons.whatshot, color: Colors.orange),
                  title: Text('Chat with Spark'),
                  subtitle: Text('15 min - Animals vocabulary'),
                  trailing: Text('Today'),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _CoursewareTab extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          ElevatedButton.icon(
            onPressed: () {
              // TODO: file picker + upload to API
            },
            icon: const Icon(Icons.upload_file),
            label: const Text('Upload Courseware'),
          ),
          const SizedBox(height: 16),
          Expanded(
            child: ListView(
              children: const [
                // TODO: list from API
                ListTile(
                  leading: Icon(Icons.description),
                  title: Text('Unit 3 - Animals'),
                  subtitle: Text('Ready - 15 vocabulary items'),
                  trailing: Icon(Icons.check_circle, color: Colors.green),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _CharactersTab extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          ElevatedButton.icon(
            onPressed: () {
              // TODO: navigate to character editor
            },
            icon: const Icon(Icons.add),
            label: const Text('Create Character'),
          ),
          const SizedBox(height: 16),
          Expanded(
            child: ListView(
              children: const [
                // TODO: list from API
                ListTile(
                  leading: Icon(Icons.whatshot, color: Colors.orange),
                  title: Text('Spark (Baby Dragon)'),
                  subtitle: Text('Active - cheerful, curious'),
                  trailing: Icon(Icons.edit),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _SettingsTab extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // AI behavior controls
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('AI Behavior',
                    style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 16),
                // TODO: bind to API
                SwitchListTile(
                  title: const Text('Singing Mode'),
                  subtitle: const Text('Allow character to sing songs'),
                  value: true,
                  onChanged: (v) {},
                ),
                SwitchListTile(
                  title: const Text('Game Mode'),
                  subtitle: const Text('Include word games in conversation'),
                  value: true,
                  onChanged: (v) {},
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Session limits
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Session Limits',
                    style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 16),
                ListTile(
                  title: const Text('Daily Time Limit'),
                  subtitle: const Text('30 minutes'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {},
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 16),

        // Parent notes (real-time override)
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
                const TextField(
                  maxLines: 4,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'e.g., Focus on animal words today...',
                  ),
                ),
                const SizedBox(height: 8),
                ElevatedButton(
                  onPressed: () {
                    // TODO: save to API
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
}
