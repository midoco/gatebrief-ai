from typing import Literal
from pydantic import BaseModel, Field


class FlightDocument(BaseModel):
    document_type: str
    present: bool = True
    flight_number: str | None = None
    origin: str | None = None
    destination: str | None = None
    departure_time: str | None = None
    aircraft_registration: str | None = None
    revision: int | None = None
    service: str | None = None
    confirmed: bool | None = None
    source_ref: str | None = None
    notes: str | None = None


class FlightProfile(BaseModel):
    required_documents: list[str] = Field(
        default_factory=lambda: [
            "operational_flight_plan",
            "ground_handling_confirmation",
            "load_or_mass_balance",
            "fuel_confirmation",
        ]
    )
    required_services: list[str] = Field(default_factory=list)
    external_checks: list[str] = Field(default_factory=list)
    latest_document_revisions: dict[str, int] = Field(default_factory=dict)


class FlightCase(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: str
    aircraft_registration: str
    profile: FlightProfile = Field(default_factory=FlightProfile)
    documents: list[FlightDocument] = Field(default_factory=list)
    research_query: str | None = None


class Finding(BaseModel):
    severity: Literal["info", "warning", "critical"]
    code: str
    message: str
    source: str = "rules"
    document_type: str | None = None
    expected_value: str | None = None
    found_value: str | None = None
    evidence_ref: str | None = None


class ResearchSource(BaseModel):
    title: str
    url: str
    content: str | None = None


class ReadinessBrief(BaseModel):
    flight_number: str
    status: Literal["READY_FOR_HUMAN_REVIEW", "ATTENTION_REQUIRED"]
    findings: list[Finding]
    sources: list[ResearchSource] = Field(default_factory=list)
    external_checks_requested: list[str] = Field(default_factory=list)
    ai_summary: str
    recommended_actions: list[str]
    model_used: str | None = None
    disclaimer: str = (
        "Decision-support only. GateBrief AI does not issue flight safety or operational clearance; "
        "authorized personnel must review and decide."
    )
