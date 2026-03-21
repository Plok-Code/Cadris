"""Logo generation for Expert plan using DALL-E 3.

Generates project logo variants based on the project brief and name.
Results are stored as mission artifacts accessible via the control-plane.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import openai
from openai import AsyncOpenAI

from .config import settings

logger = logging.getLogger(__name__)


@dataclass
class GeneratedLogo:
    """A single generated logo variant."""
    url: str
    revised_prompt: str
    style: str


async def generate_logos(
    project_name: str,
    project_brief: str,
    num_variants: int = 3,
) -> list[GeneratedLogo]:
    """Generate logo variants using DALL-E 3.

    Returns a list of GeneratedLogo with temporary URLs (valid ~1 hour).
    The caller should download and persist the images.

    Args:
        project_name: Name of the project
        project_brief: Short description (will be truncated to 200 chars)
        num_variants: Number of variants to generate (1-4)
    """
    if not settings.openai_api_key:
        logger.warning("OPENAI_API_KEY not set, skipping logo generation")
        return []

    brief = project_brief[:200]
    num_variants = min(max(num_variants, 1), 4)

    styles = [
        ("modern minimalist", "Clean, modern, minimalist logo"),
        ("geometric abstract", "Abstract geometric shapes, bold colors"),
        ("professional corporate", "Professional, corporate, trustworthy"),
        ("playful startup", "Playful, vibrant, startup-friendly"),
    ][:num_variants]

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    logos: list[GeneratedLogo] = []

    for style_key, style_desc in styles:
        prompt = (
            f"Create a professional logo for '{project_name}'. "
            f"Project: {brief}. "
            f"Style: {style_desc}. "
            "The logo should work on white and dark backgrounds. "
            "No text in the logo unless it's the project name integrated into the design. "
            "Square format, centered, with transparent-friendly composition."
        )

        try:
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image = response.data[0]
            logos.append(GeneratedLogo(
                url=image.url or "",
                revised_prompt=image.revised_prompt or prompt,
                style=style_key,
            ))
            logger.info("Generated logo variant '%s' for project '%s'", style_key, project_name)

        except openai.OpenAIError as exc:
            logger.warning("Logo generation failed for style '%s': %s", style_key, exc)

    return logos
