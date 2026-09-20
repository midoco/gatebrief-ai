# Devpost Draft

## Project name
GateBrief AI

## Tagline
Rules verify. Nemotron reasons. Tavily grounds. Humans decide.

## One-line description
An agentic aviation operations assistant that turns fragmented flight information into a source-backed, human-reviewed operational readiness brief.

## Problem
Airline and ground-operations teams often assemble flight information from multiple documents, messages, confirmations, and current external sources. Missing or conflicting data can be difficult to spot quickly, especially when time is limited.

## Solution
GateBrief AI combines deterministic validation rules, NVIDIA Nemotron reasoning through Nebius Token Factory, and optional Tavily live research. It detects missing items and contradictions, gathers current supporting information when needed, and produces a concise readiness brief with actions for authorized human review.

## Safety boundary
GateBrief AI is decision-support software. It does not issue flight safety clearance, dispatch authority, or operational certification.

## Technology
- Flutter web interface
- FastAPI backend
- Nebius Token Factory
- NVIDIA Nemotron
- Tavily search
- Structured synthetic aviation demo data

## What makes it agentic
The application executes a multi-step workflow: validate -> identify uncertainty -> research when necessary -> reason across findings and sources -> produce an action-oriented brief -> request human review.
