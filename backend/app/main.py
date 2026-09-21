import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import FlightCase, ReadinessBrief
from app.services.orchestrator import GateBriefOrchestrator

app = FastAPI(
    title="GateBrief AI API",
    version="0.2.0",
    description="Human-in-the-loop aviation operations readiness assistant for the Nebius x NVIDIA Global AI Hackathon.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = GateBriefOrchestrator()
SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent / "sample_data"
SCENARIOS = {
    "missing-service": {
        "file": "scenarios/01_missing_service.json",
        "label": "Missing service confirmation",
        "description": "Catering is required for the flight but has no positive confirmation.",
    },
    "time-conflict": {
        "file": "scenarios/02_departure_time_mismatch.json",
        "label": "Departure time conflict",
        "description": "Ground handling references a different departure time than the operational case.",
    },
    "aircraft-conflict": {
        "file": "scenarios/03_aircraft_mismatch.json",
        "label": "Aircraft registration conflict",
        "description": "A load/mass-balance record references a different aircraft registration.",
    },
    "stale-revision": {
        "file": "scenarios/04_stale_revision.json",
        "label": "Stale document revision",
        "description": "A handling confirmation is older than the expected operational revision.",
    },
    "external-checks": {
        "file": "scenarios/05_external_checks.json",
        "label": "Fresh external checks",
        "description": "The flight folder is internally consistent but asks for fresh weather, NOTAM, and airport context.",
    },
}


def _load_case(relative_path: str) -> FlightCase:
    path = SAMPLE_DATA_DIR / relative_path
    return FlightCase(**json.loads(path.read_text(encoding="utf-8")))


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "gatebrief-api", "version": "0.2.0"}


@app.post("/api/v1/brief", response_model=ReadinessBrief)
def create_brief(case: FlightCase) -> ReadinessBrief:
    try:
        return orchestrator.run(case)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Brief generation failed: {exc}") from exc


@app.get("/api/v1/demo", response_model=ReadinessBrief)
def demo_brief() -> ReadinessBrief:
    return orchestrator.run(_load_case("flight_case.json"))


@app.get("/api/v1/scenarios")
def list_scenarios() -> list[dict[str, str]]:
    return [
        {"id": scenario_id, "label": meta["label"], "description": meta["description"]}
        for scenario_id, meta in SCENARIOS.items()
    ]


@app.get("/api/v1/scenarios/{scenario_id}", response_model=ReadinessBrief)
def run_scenario(scenario_id: str) -> ReadinessBrief:
    meta = SCENARIOS.get(scenario_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Unknown demo scenario")
    return orchestrator.run(_load_case(meta["file"]))
