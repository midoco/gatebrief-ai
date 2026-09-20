class Finding {
  final String severity;
  final String code;
  final String message;
  final String source;

  Finding({required this.severity, required this.code, required this.message, required this.source});

  factory Finding.fromJson(Map<String, dynamic> json) => Finding(
        severity: json['severity'] ?? 'info',
        code: json['code'] ?? '',
        message: json['message'] ?? '',
        source: json['source'] ?? 'rules',
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

  ReadinessBrief({
    required this.flightNumber,
    required this.status,
    required this.aiSummary,
    required this.disclaimer,
    required this.findings,
    required this.recommendedActions,
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
      );
}
