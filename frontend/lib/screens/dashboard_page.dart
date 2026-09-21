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
  List<ScenarioOption> _scenarios = [];
  String? _selectedScenarioId;
  String? _error;
  bool _loading = false;
  bool _loadingScenarios = true;

  @override
  void initState() {
    super.initState();
    _loadScenarios();
  }

  Future<void> _loadScenarios() async {
    try {
      final scenarios = await _api.loadScenarios();
      if (!mounted) return;
      setState(() {
        _scenarios = scenarios;
        _selectedScenarioId = scenarios.isEmpty ? null : scenarios.first.id;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _loadingScenarios = false);
    }
  }

  Future<void> _runScenario() async {
    final scenarioId = _selectedScenarioId;
    if (scenarioId == null) return;

    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final brief = await _api.loadScenario(scenarioId);
      if (mounted) setState(() => _brief = brief);
    } catch (e) {
      if (mounted) setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final selected = _scenarios.where((s) => s.id == _selectedScenarioId).firstOrNull;

    return Scaffold(
      appBar: AppBar(title: const Text('GateBrief AI')),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 980),
          child: ListView(
            padding: const EdgeInsets.all(24),
            children: [
              Text(
                'Flight readiness, grounded and human-reviewed',
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              const SizedBox(height: 8),
              const Text('Rules verify. Nemotron reasons. Tavily grounds. Humans decide.'),
              const SizedBox(height: 24),
              DropdownButtonFormField<String>(
                value: _selectedScenarioId,
                decoration: const InputDecoration(
                  labelText: 'Operational scenario',
                  border: OutlineInputBorder(),
                ),
                items: _scenarios
                    .map((scenario) => DropdownMenuItem(
                          value: scenario.id,
                          child: Text(scenario.label),
                        ))
                    .toList(),
                onChanged: (_loading || _loadingScenarios)
                    ? null
                    : (value) => setState(() {
                          _selectedScenarioId = value;
                          _brief = null;
                        }),
              ),
              if (selected != null) ...[
                const SizedBox(height: 8),
                Text(selected.description, style: Theme.of(context).textTheme.bodySmall),
              ],
              const SizedBox(height: 16),
              FilledButton.icon(
                onPressed: (_loading || _loadingScenarios || _selectedScenarioId == null) ? null : _runScenario,
                icon: const Icon(Icons.flight_takeoff),
                label: Text(_loading ? 'Running GateBrief...' : 'Run selected scenario'),
              ),
              if (_error != null) ...[
                const SizedBox(height: 16),
                Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
              ],
              if (_brief != null) ...[
                const SizedBox(height: 24),
                _StatusCard(brief: _brief!),
                const SizedBox(height: 16),
                Text('Findings & evidence', style: Theme.of(context).textTheme.titleLarge),
                ..._brief!.findings.map((f) => _FindingCard(finding: f)),
                if (_brief!.externalChecksRequested.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  Text('External checks requested', style: Theme.of(context).textTheme.titleLarge),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: _brief!.externalChecksRequested.map((item) => Chip(label: Text(item))).toList(),
                  ),
                ],
                const SizedBox(height: 16),
                Text('Recommended actions', style: Theme.of(context).textTheme.titleLarge),
                ..._brief!.recommendedActions.map(
                  (a) => ListTile(
                    leading: const Icon(Icons.check_circle_outline),
                    title: Text(a),
                  ),
                ),
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

class _FindingCard extends StatelessWidget {
  const _FindingCard({required this.finding});
  final Finding finding;

  @override
  Widget build(BuildContext context) {
    final icon = finding.severity == 'critical'
        ? Icons.error
        : finding.severity == 'warning'
            ? Icons.warning
            : Icons.info;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon),
                const SizedBox(width: 10),
                Expanded(child: Text(finding.code, style: Theme.of(context).textTheme.titleMedium)),
              ],
            ),
            const SizedBox(height: 8),
            Text(finding.message),
            if (finding.expectedValue != null || finding.foundValue != null) ...[
              const SizedBox(height: 10),
              Text('Expected: ${finding.expectedValue ?? '-'}'),
              Text('Found: ${finding.foundValue ?? '-'}'),
            ],
            if (finding.evidenceRef != null) ...[
              const SizedBox(height: 8),
              Text('Evidence: ${finding.evidenceRef}', style: Theme.of(context).textTheme.bodySmall),
            ],
          ],
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
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('${brief.flightNumber} - ${brief.status}', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 12),
            Text(brief.aiSummary),
            if (brief.modelUsed != null) ...[
              const SizedBox(height: 12),
              Text('Nebius model: ${brief.modelUsed}', style: Theme.of(context).textTheme.bodySmall),
            ],
          ],
        ),
      ),
    );
  }
}

extension _FirstOrNull<T> on Iterable<T> {
  T? get firstOrNull => isEmpty ? null : first;
}
