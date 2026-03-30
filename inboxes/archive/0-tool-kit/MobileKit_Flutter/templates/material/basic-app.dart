import 'package:flutter/material.dart';

void main() {
  runApp(const MyFlutterApp());
}

class MyFlutterApp extends StatelessWidget {
  const MyFlutterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MobileKit Flutter',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.light,
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.dark,
        ),
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final List<Feature> features = [
    Feature(
      icon: Icons.psychology,
      title: 'AI Agents',
      description: '12 specialized AI agents for Flutter development',
      color: Colors.purple,
    ),
    Feature(
      icon: Icons.widgets,
      title: 'Flutter Widgets',
      description: 'Production-ready Material Design components',
      color: Colors.blue,
    ),
    Feature(
      icon: Icons.verified,
      title: 'Testing Suite',
      description: 'Widget, integration, and golden tests',
      color: Colors.green,
    ),
    Feature(
      icon: Icons.store,
      title: 'Multi-Store Ready',
      description: 'Deploy to Google Play and App Store',
      color: Colors.orange,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MobileKit Flutter'),
        centerTitle: true,
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Card(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  children: [
                    Icon(
                      Icons.rocket_launch,
                      size: 60,
                      color: Theme.of(context).colorScheme.primary,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Welcome to MobileKit Flutter',
                      style: Theme.of(context).textTheme.headlineSmall,
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'AI-Powered Cross-Platform Development',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Features Section
            Text(
              'Features',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),

            // Features List
            ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: features.length,
              separatorBuilder: (context, index) => const SizedBox(height: 12),
              itemBuilder: (context, index) {
                return FeatureCard(feature: features[index]);
              },
            ),

            const SizedBox(height: 32),

            // Get Started Button
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: () {
                  _showGetStartedDialog(context);
                },
                icon: const Icon(Icons.play_arrow),
                label: const Text('Get Started'),
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showGetStartedDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('🚀 Getting Started'),
        content: const Text(
          'Ready to start Flutter development with MobileKit!\n\n'
          'Use the CLI tool to generate features:\n'
          'mkf generate-feature --name user_profile',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Got it!'),
          ),
        ],
      ),
    );
  }
}

class FeatureCard extends StatelessWidget {
  final Feature feature;

  const FeatureCard({
    super.key,
    required this.feature,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: feature.color.withOpacity(0.1),
          child: Icon(
            feature.icon,
            color: feature.color,
          ),
        ),
        title: Text(feature.title),
        subtitle: Text(feature.description),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: () {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('${feature.title} feature tapped!'),
              behavior: SnackBarBehavior.floating,
            ),
          );
        },
      ),
    );
  }
}

// Models
class Feature {
  final IconData icon;
  final String title;
  final String description;
  final Color color;

  Feature({
    required this.icon,
    required this.title,
    required this.description,
    required this.color,
  });
}
