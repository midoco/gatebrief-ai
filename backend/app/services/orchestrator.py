from app.schemas import FlightCase, ReadinessBrief
from app.services.rules import validate_case
from app.services.nebius_client import NebiusService
from app.services.tavily_client import TavilyService


class GateBriefOrchestrator:
    def __init__(self) -> None:
        self.nebius = NebiusService()
        self.tavily = TavilyService()

    @staticmethod
    def _research_query(case: FlightCase) -> str | None:
        if case.research_query:
            return case.research_query
        if not case.profile.external_checks:
            return None
        checks = ", ".join(case.profile.external_checks)
        return (
            f"Current operational context for flight {case.flight_number} "
            f"from {case.origin} to {case.destination}: {checks}"
        )

    def run(self, case: FlightCase) -> ReadinessBrief:
        findings = validate_case(case)
        sources = self.tavily.search(self._research_query(case))
        summary, actions, model = self.nebius.summarize(case, findings, sources)

        needs_attention = any(f.severity in {"warning", "critical"} for f in findings)
        return ReadinessBrief(
            flight_number=case.flight_number,
            status="ATTENTION_REQUIRED" if needs_attention else "READY_FOR_HUMAN_REVIEW",
            findings=findings,
            sources=sources,
            external_checks_requested=case.profile.external_checks,
            ai_summary=summary,
            recommended_actions=actions,
            model_used=model,
        )
