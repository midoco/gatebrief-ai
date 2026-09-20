import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import FlightCase, ReadinessBrief
from app.services.orchestrator import GateBriefOrchestrator

app = FastAPI(
    title="GateBrief AI API",
    version="0.1.0",
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


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "gatebrief-api", "version": "0.1.0"}


@app.post("/api/v1/brief", response_model=ReadinessBrief)
def create_brief(case: FlightCase) -> ReadinessBrief:
    try:
        return orchestrator.run(case)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Brief generation failed: {exc}") from exc


@app.get("/api/v1/demo", response_model=ReadinessBrief)
def demo_brief() -> ReadinessBrief:
    path = Path(__file__).resolve().parent.parent / "sample_data" / "flight_case.json"
    case = FlightCase(**json.loads(path.read_text(encoding="utf-8")))
    return orchestrator.run(case)
