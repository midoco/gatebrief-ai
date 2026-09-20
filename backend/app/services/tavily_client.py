from tavily import TavilyClient
from app.config import settings
from app.schemas import ResearchSource


class TavilyService:
    def __init__(self) -> None:
        self.enabled = bool(settings.tavily_api_key and settings.enable_live_research)
        self.client = TavilyClient(api_key=settings.tavily_api_key) if self.enabled else None

    def search(self, query: str | None) -> list[ResearchSource]:
        if not self.enabled or not self.client or not query:
            return []

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=False,
        )
        sources: list[ResearchSource] = []
        for result in response.get("results", []):
            sources.append(
                ResearchSource(
                    title=str(result.get("title", "Untitled source")),
                    url=str(result.get("url", "")),
                    content=str(result.get("content", ""))[:1200],
                )
            )
        return sources
