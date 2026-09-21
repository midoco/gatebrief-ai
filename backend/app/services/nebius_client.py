import json
from openai import OpenAI
from app.config import settings
from app.schemas import FlightCase, Finding, ResearchSource


class NebiusService:
    def __init__(self) -> None:
        self.enabled = bool(settings.nebius_api_key)
        self.client = None
        self._model = settings.nebius_model.strip() or None
        if self.enabled:
            self.client = OpenAI(
                base_url=settings.nebius_base_url,
                api_key=settings.nebius_api_key,
            )

    def resolve_model(self) -> str | None:
        if not self.enabled or not self.client:
            return None
        if self._model:
            return self._model

        models = list(self.client.models.list().data)
        ids = [m.id for m in models]
        nemotron = [m for m in ids if "nemotron" in m.lower()]
        preferred = [m for m in nemotron if "super" in m.lower()]
        self._model = (preferred or nemotron or ids)[0] if ids else None
        return self._model

    def summarize(
        self,
        case: FlightCase,
        findings: list[Finding],
        sources: list[ResearchSource],
    ) -> tuple[str, list[str], str | None]:
        model = self.resolve_model()
        if not self.enabled or not self.client or not model:
            return self._fallback(findings), self._fallback_actions(findings), model

        payload = {
            "flight": case.model_dump(),
            "deterministic_findings": [f.model_dump() for f in findings],
            "research_sources": [s.model_dump() for s in sources],
        }

        response = self.client.chat.completions.create(
            model=model,
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are GateBrief AI, an aviation operations decision-support assistant. "
                        "Never claim to authorize, clear, dispatch, or certify a flight. "
                        "Use only the supplied case, deterministic findings, and supplied research sources. "
                        "Treat exact deterministic comparisons as authoritative findings. "
                        "If an external check is requested but no research source is supplied, state that it remains pending. "
                        "Return strict JSON with keys summary (string) and recommended_actions (array of strings). "
                        "Be concise, preserve evidence traceability, and explicitly flag conflicts and missing data."
                    ),
                },
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
        )

        text = response.choices[0].message.content or "{}"
        try:
            data = json.loads(text)
            summary = str(data.get("summary", "AI summary unavailable."))
            actions = [str(x) for x in data.get("recommended_actions", [])]
            return summary, actions, model
        except json.JSONDecodeError:
            return text, self._fallback_actions(findings), model

    @staticmethod
    def _fallback(findings: list[Finding]) -> str:
        problems = [f for f in findings if f.severity in {"warning", "critical"}]
        pending_external = [f for f in findings if f.code == "EXTERNAL_CHECK_REQUIRED"]
        if problems:
            return f"GateBrief detected {len(problems)} item(s) requiring human attention."
        if pending_external:
            return (
                f"Internal deterministic checks are clear; {len(pending_external)} fresh external check(s) "
                "remain pending before human review."
            )
        return "Deterministic checks found no blocking inconsistencies. Human review is still required."

    @staticmethod
    def _fallback_actions(findings: list[Finding]) -> list[str]:
        actions: list[str] = []
        for item in findings:
            if item.code == "MISSING_DOCUMENT":
                actions.append("Obtain or verify the missing document before closing the flight folder.")
            elif item.code == "MISSING_SERVICE_CONFIRMATION":
                actions.append("Confirm the required operational service or record an approved exception.")
            elif item.code == "STALE_DOCUMENT_REVISION":
                actions.append("Replace the stale document with the latest approved revision and re-run checks.")
            elif item.code == "DUPLICATE_DOCUMENT_CONFLICT":
                actions.append("Resolve duplicate conflicting documents against the authoritative operational record.")
            elif item.code.endswith("MISMATCH"):
                actions.append("Resolve the conflicting flight data against the authoritative operational record.")
            elif item.code == "EXTERNAL_CHECK_REQUIRED":
                actions.append("Obtain fresh external evidence for the requested operational context before final review.")
        return list(dict.fromkeys(actions)) or ["Perform authorized human review of the flight folder."]
