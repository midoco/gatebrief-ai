# GateBrief AI Architecture

## Core principle

**Rules verify. Nemotron reasons. Tavily grounds. Humans decide.**

## Workflow

1. Ingest a synthetic/demo flight case and operational documents.
2. Normalize the case into structured fields.
3. Run deterministic validations for missing documents and cross-document mismatches.
4. Trigger live research only when current external information is required.
5. Send the structured case, rule findings, and retrieved sources to an NVIDIA Nemotron model through Nebius Token Factory.
6. Generate a concise readiness brief and recommended actions.
7. Present everything to an authorized human reviewer; the system never grants operational or safety clearance.
8. Preserve source/model/tool metadata for auditability.

## Hackathon alignment

- Nebius runtime: Token Factory OpenAI-compatible API.
- NVIDIA model: an available Nemotron model selected from the user's account.
- Agentic workflow: deterministic rules + conditional research + reasoning + briefing.
- Tavily: live sourced research for a secondary sponsor-prize path.
- Human-in-the-loop: explicit review boundary for a high-stakes domain.
