# GateBrief AI - Rules Engine V2 update

This update is intended to be copied over the existing repository root.

## Included changes

- Configurable `FlightProfile` per flight case.
- Deterministic checks for required documents and services.
- Flight number, aircraft, origin, destination, and departure-time consistency checks.
- Stale revision detection.
- Conflicting duplicate document detection.
- Evidence metadata (`expected_value`, `found_value`, `evidence_ref`).
- External-check requests for weather/NOTAM/airport context.
- Five synthetic operational scenarios.
- Scenario API endpoints and Flutter scenario selector.
- Improved Nebius fallback summaries/actions.
- Six backend rules tests.

## Apply locally

1. Extract this ZIP.
2. Copy the contents into the root of your existing `gatebrief-ai` folder and allow replacement of matching files.
3. From `backend`, run `pytest -q`.
4. Start FastAPI with `uvicorn app.main:app --reload`.
5. Open `/docs` and test `GET /api/v1/scenarios` and a scenario endpoint.
6. Run Flutter and test the scenario selector.
7. In GitHub Desktop, review the changes, commit with `Add configurable Rules Engine V2 scenarios`, then push.

The backend rules included here were locally tested: 6 tests passed.
