import 'package:flutter/material.dart';
import 'screens/dashboard_page.dart';

void main() => runApp(const GateBriefApp());

class GateBriefApp extends StatelessWidget {
  const GateBriefApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'GateBrief AI',
      theme: ThemeData(useMaterial3: true, brightness: Brightness.dark),
      home: const DashboardPage(),
    );
  }
}
