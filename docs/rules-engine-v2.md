# Rules Engine V2

GateBrief separates deterministic verification from AI reasoning.

## Why deterministic rules exist

Fields such as flight number, aircraft registration, route, departure time, required-document presence, and revision numbers should not be guessed by an LLM. GateBrief checks them deterministically first and attaches evidence references to each finding.

## What V2 checks

- required flight documents;
- required service confirmations;
- flight-number consistency;
- aircraft-registration consistency;
- origin and destination consistency;
- departure-time consistency;
- stale document revisions;
- conflicting duplicate documents;
- external checks that require fresh evidence.

## Flight profile

Requirements are defined per flight case instead of being hardcoded globally. This allows a demo or future airline integration to configure documents, services, and external checks by flight type, station, route, or operator procedure.

## AI boundary

Nemotron is expected to reason over deterministic findings and research evidence, not replace exact comparisons. Tavily is used only when fresh external context is requested. Weather/NOTAM-style context remains decision support and should use authoritative operational sources in any production airline deployment.

## Demo scenarios

The repository includes synthetic scenarios for missing service confirmation, departure-time conflict, aircraft conflict, stale revision, and fresh external checks. No real airline or passenger data is used.
