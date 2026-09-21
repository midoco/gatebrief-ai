class Finding {
  final String severity;
  final String code;
  final String message;
  final String source;
  final String? documentType;
  final String? expectedValue;
  final String? foundValue;
  final String? evidenceRef;

  Finding({
    required this.severity,
    required this.code,
    required this.message,
    required this.source,
    this.documentType,
    this.expectedValue,
    this.foundValue,
    this.evidenceRef,
  });

  factory Finding.fromJson(Map<String, dynamic> json) => Finding(
        severity: json['severity'] ?? 'info',
        code: json['code'] ?? '',
        message: json['message'] ?? '',
        source: json['source'] ?? 'rules',
        documentType: json['document_type'],
        expectedValue: json['expected_value'],
        foundValue: json['found_value'],
        evidenceRef: json['evidence_ref'],
      );
}

class ScenarioOption {
  final String id;
  final String label;
  final String description;

  ScenarioOption({required this.id, required this.label, required this.description});

  factory ScenarioOption.fromJson(Map<String, dynamic> json) => ScenarioOption(
        id: json['id'] ?? '',
        label: json['label'] ?? '',
        description: json['description'] ?? '',
      );
}

class ReadinessBrief {
  final String flightNumber;
  final String status;
  final String aiSummary;
  final String disclaimer;
  final String? modelUsed;
  final List<Finding> findings;
  final List<String> recommendedActions;
  final List<String> externalChecksRequested;

  ReadinessBrief({
    required this.flightNumber,
    required this.status,
    required this.aiSummary,
    required this.disclaimer,
    required this.findings,
    required this.recommendedActions,
    required this.externalChecksRequested,
    this.modelUsed,
  });

  factory ReadinessBrief.fromJson(Map<String, dynamic> json) => ReadinessBrief(
        flightNumber: json['flight_number'] ?? '',
        status: json['status'] ?? '',
        aiSummary: json['ai_summary'] ?? '',
        disclaimer: json['disclaimer'] ?? '',
        modelUsed: json['model_used'],
        findings: (json['findings'] as List? ?? [])
            .map((e) => Finding.fromJson(Map<String, dynamic>.from(e)))
            .toList(),
        recommendedActions: (json['recommended_actions'] as List? ?? []).map((e) => e.toString()).toList(),
        externalChecksRequested:
            (json['external_checks_requested'] as List? ?? []).map((e) => e.toString()).toList(),
      );
}
