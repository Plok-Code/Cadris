"""Build self-contained HTML for shared dossier viewing."""
from __future__ import annotations

from html import escape

from ..models import RendererRequest
from .render_service import render_safe_markdown_html


def build_shared_html(payload: RendererRequest) -> str:
    """Build a self-contained HTML page for shared dossier viewing."""
    css = """
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; color: #1a1a2e; line-height: 1.6; }
    h1 { font-size: 1.5rem; color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 0.5rem; }
    h2 { font-size: 1.1rem; color: #0f3460; margin-top: 1.5rem; }
    .quality-label { font-size: 0.9rem; color: #0f3460; padding: 0.25rem 0.5rem; background: #f0f4f8; border-left: 3px solid #0f3460; margin-bottom: 1rem; }
    .certainty-tag { display: inline-block; font-size: 0.7rem; padding: 0.1rem 0.4rem; border-radius: 3px; color: #fff; margin-left: 0.5rem; vertical-align: middle; }
    .certainty-solid { background: #2ecc71; }
    .certainty-to_confirm { background: #f39c12; }
    .certainty-unknown { background: #95a5a6; }
    .certainty-blocking { background: #e74c3c; }
    .footer { margin-top: 2rem; padding-top: 0.5rem; border-top: 1px solid #ddd; font-size: 0.75rem; color: #999; }
    """

    cert_labels = {"solid": "Solide", "to_confirm": "A confirmer", "unknown": "Inconnu", "blocking": "Bloquant"}

    safe_title = escape(payload.title)
    safe_summary = escape(payload.summary)
    parts = [f"<h1>{safe_title}</h1>"]
    if payload.quality_label:
        parts.append(
            f'<p class="quality-label"><strong>Statut qualite</strong> : {escape(payload.quality_label)}</p>'
        )
    parts.append(f"<p>{safe_summary}</p>")
    for section in payload.sections:
        certainty_class = f"certainty-{section.certainty}"
        cert_label = cert_labels.get(section.certainty, section.certainty)
        tag = f'<span class="certainty-tag {certainty_class}">{escape(cert_label)}</span>'
        parts.append(f"<h2>{escape(section.title)} {tag}</h2>")
        parts.append(render_safe_markdown_html(section.content))
    parts.append('<div class="footer">Partage via Cadris - lien revocable par le proprietaire</div>')

    body = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>{safe_title} - Cadris</title><style>{css}</style></head>
<body>{body}</body>
</html>"""
