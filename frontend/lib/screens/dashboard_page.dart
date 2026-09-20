import 'package:flutter/material.dart';
import '../models/brief.dart';
import '../services/api_service.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final _api = ApiService();
  ReadinessBrief? _brief;
  String? _error;
  bool _loading = false;

  Future<void> _runDemo() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final brief = await _api.loadDemo();
      setState(() => _brief = brief);
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('GateBrief AI')),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 980),
          child: ListView(
            padding: const EdgeInsets.all(24),
            children: [
              Text('Flight readiness, grounded and human-reviewed', style: Theme.of(context).textTheme.headlineMedium),
              const SizedBox(height: 8),
              const Text('Rules verify. Nemotron reasons. Tavily grounds. Humans decide.'),
              const SizedBox(height: 24),
              FilledButton.icon(
                onPressed: _loading ? null : _runDemo,
                icon: const Icon(Icons.flight_takeoff),
                label: Text(_loading ? 'Running GateBrief…' : 'Run demo flight GB451'),
              ),
              if (_error != null) ...[
                const SizedBox(height: 16),
                Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
              ],
              if (_brief != null) ...[
                const SizedBox(height: 24),
                _StatusCard(brief: _brief!),
                const SizedBox(height: 16),
                Text('Findings', style: Theme.of(context).textTheme.titleLarge),
                ..._brief!.findings.map((f) => Card(
                      child: ListTile(
                        leading: Icon(f.severity == 'critical' ? Icons.error : f.severity == 'warning' ? Icons.warning : Icons.info),
                        title: Text(f.code),
                        subtitle: Text(f.message),
                      ),
                    )),
                const SizedBox(height: 16),
                Text('Recommended actions', style: Theme.of(context).textTheme.titleLarge),
                ..._brief!.recommendedActions.map((a) => ListTile(leading: const Icon(Icons.check_circle_outline), title: Text(a))),
                const SizedBox(height: 16),
                Text(_brief!.disclaimer, style: Theme.of(context).textTheme.bodySmall),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class _StatusCard extends StatelessWidget {
  const _StatusCard({required this.brief});
  final ReadinessBrief brief;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('${brief.flightNumber} — ${brief.status}', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          Text(brief.aiSummary),
          if (brief.modelUsed != null) ...[
            const SizedBox(height: 12),
            Text('Nebius model: ${brief.modelUsed}', style: Theme.of(context).textTheme.bodySmall),
          ],
        ]),
      ),
    );
  }
}
