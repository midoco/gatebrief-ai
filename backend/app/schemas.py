from typing import Literal
from pydantic import BaseModel, Field


class FlightDocument(BaseModel):
    document_type: str
    present: bool = True
    flight_number: str | None = None
    departure_time: str | None = None
    aircraft_registration: str | None = None
    notes: str | None = None


class FlightCase(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: str
    aircraft_registration: str
    documents: list[FlightDocument] = Field(default_factory=list)
    research_query: str | None = None


class Finding(BaseModel):
    severity: Literal["info", "warning", "critical"]
    code: str
    message: str
    source: str = "rules"


class ResearchSource(BaseModel):
    title: str
    url: str
    content: str | None = None


class ReadinessBrief(BaseModel):
    flight_number: str
    status: Literal["READY_FOR_HUMAN_REVIEW", "ATTENTION_REQUIRED"]
    findings: list[Finding]
    sources: list[ResearchSource] = Field(default_factory=list)
    ai_summary: str
    recommended_actions: list[str]
    model_used: str | None = None
    disclaimer: str = (
        "Decision-support only. GateBrief AI does not issue flight safety or operational clearance; "
        "authorized personnel must review and decide."
    )
