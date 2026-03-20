"""Perplexity web research for Pro/Expert plans.

Provides real-time web research via Perplexity Sonar API before agent execution.
Results are injected into the agent's context to ground outputs in real data.

- Pro plan: Perplexity Sonar (fast web search)
- Expert plan: Perplexity Sonar Pro (deep research)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


@dataclass
class WebResearchResult:
    """Result of a Perplexity web search."""
    query: str
    content: str
    citations: list[str]
    model_used: str


def _get_api_key() -> str | None:
    return os.getenv("PERPLEXITY_API_KEY")


def get_research_model(plan: str) -> str | None:
    """Return the Perplexity model for the given plan, or None if not available."""
    if plan == "expert":
        return "sonar-pro"
    if plan == "pro":
        return "sonar"
    return None


def build_research_queries(agent_code: str, intake_text: str) -> list[str]:
    """Build targeted research queries for an agent based on the project intake.

    Returns 1-3 queries tailored to the agent's domain.
    """
    # Truncate intake for query building
    brief = intake_text[:500]

    if agent_code == "business":
        return [
            f"market size and competitors for: {brief}",
            f"pricing benchmarks and business models in the industry of: {brief}",
        ]
    if agent_code == "strategy":
        return [
            f"industry trends and opportunities for: {brief}",
        ]
    if agent_code in ("tech_arch", "tech_data"):
        return [
            f"best technology stack and architecture patterns for: {brief}",
        ]
    return []


async def research(
    query: str,
    model: str = "sonar",
) -> WebResearchResult | None:
    """Execute a single Perplexity web search.

    Returns None if the API key is not configured or the request fails.
    """
    api_key = _get_api_key()
    if not api_key:
        logger.debug("PERPLEXITY_API_KEY not set, skipping web research")
        return None

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                PERPLEXITY_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a research assistant. Provide concise, factual answers "
                                "with specific numbers, market data, and sources. "
                                "Focus on actionable business and technology insights. "
                                "Answer in French."
                            ),
                        },
                        {"role": "user", "content": query},
                    ],
                },
            )
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"]
        citations = data.get("citations", [])

        return WebResearchResult(
            query=query,
            content=content,
            citations=citations,
            model_used=model,
        )

    except Exception as exc:
        logger.warning("Perplexity research failed for query '%s': %s", query[:80], exc)
        return None


async def research_for_agent(
    agent_code: str,
    intake_text: str,
    plan: str,
) -> str:
    """Run web research for an agent and return formatted context string.

    Returns empty string if research is not available for this plan/agent.
    """
    model = get_research_model(plan)
    if model is None:
        return ""

    queries = build_research_queries(agent_code, intake_text)
    if not queries:
        return ""

    results: list[WebResearchResult] = []
    for query in queries:
        result = await research(query, model=model)
        if result:
            results.append(result)

    if not results:
        return ""

    # Format as context section
    sections = ["## Recherche web (sources reelles)"]
    all_citations: list[str] = []

    for r in results:
        sections.append(f"### {r.query}")
        sections.append(r.content)
        all_citations.extend(r.citations)

    if all_citations:
        sections.append("### Sources")
        for i, citation in enumerate(all_citations[:10], 1):
            sections.append(f"{i}. {citation}")

    return "\n\n".join(sections)
