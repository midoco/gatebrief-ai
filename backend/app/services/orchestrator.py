from app.schemas import FlightCase, ReadinessBrief
from app.services.rules import validate_case
from app.services.nebius_client import NebiusService
from app.services.tavily_client import TavilyService


class GateBriefOrchestrator:
    def __init__(self) -> None:
        self.nebius = NebiusService()
        self.tavily = TavilyService()

    def run(self, case: FlightCase) -> ReadinessBrief:
        findings = validate_case(case)
        sources = self.tavily.search(case.research_query)
        summary, actions, model = self.nebius.summarize(case, findings, sources)

        needs_attention = any(f.severity in {"warning", "critical"} for f in findings)
        return ReadinessBrief(
            flight_number=case.flight_number,
            status="ATTENTION_REQUIRED" if needs_attention else "READY_FOR_HUMAN_REVIEW",
            findings=findings,
            sources=sources,
            ai_summary=summary,
            recommended_actions=actions,
            model_used=model,
        )
