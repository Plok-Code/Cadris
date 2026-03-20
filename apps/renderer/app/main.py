from __future__ import annotations

import io
import logging
from html import escape

import bleach
import markdown as md_lib
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DossierSection(BaseModel):
    id: str
    title: str
    content: str
    certainty: str


class RendererRequest(BaseModel):
    title: str
    summary: str
    quality_label: str | None = None
    sections: list[DossierSection]


class RendererResponse(BaseModel):
    markdown: str


class HtmlResponse(BaseModel):
    html: str


app = FastAPI(title="Cadris Renderer", version="0.1.0")


CSS_TEMPLATE = """
@page { size: A4; margin: 2cm; }
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a2e;
}
h1 {
    font-size: 20pt;
    color: #16213e;
    border-bottom: 2px solid #0f3460;
    padding-bottom: 8pt;
    margin-bottom: 16pt;
}
h2 {
    font-size: 14pt;
    color: #0f3460;
    margin-top: 18pt;
    margin-bottom: 8pt;
}
h3 {
    font-size: 12pt;
    color: #16213e;
    margin-top: 14pt;
    margin-bottom: 6pt;
}
p {
    margin-bottom: 10pt;
}
ul, ol {
    margin-bottom: 10pt;
    padding-left: 20pt;
}
li {
    margin-bottom: 4pt;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 12pt;
    font-size: 10pt;
}
th, td {
    border: 1px solid #ccc;
    padding: 6pt 8pt;
    text-align: left;
    vertical-align: top;
}
th {
    background: #f0f4f8;
    font-weight: 600;
    color: #0f3460;
}
tr:nth-child(even) td {
    background: #fafbfc;
}
code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
    background: #f0f4f8;
    padding: 1pt 4pt;
    border-radius: 2pt;
}
pre {
    background: #f0f4f8;
    padding: 8pt 12pt;
    border-radius: 4pt;
    font-size: 9pt;
    overflow-x: auto;
    margin-bottom: 10pt;
}
pre code {
    background: none;
    padding: 0;
}
blockquote {
    border-left: 3pt solid #0f3460;
    margin: 10pt 0;
    padding: 4pt 12pt;
    color: #555;
    background: #f8f9fa;
}
.certainty-tag {
    display: inline-block;
    font-size: 8pt;
    padding: 2pt 6pt;
    border-radius: 3pt;
    color: #fff;
    margin-left: 8pt;
    vertical-align: middle;
}
.certainty-solid { background: #2ecc71; }
.certainty-to_confirm { background: #f39c12; }
.certainty-unknown { background: #95a5a6; }
.certainty-blocking { background: #e74c3c; }
.quality-label {
    font-size: 10pt;
    color: #0f3460;
    margin-bottom: 12pt;
    padding: 4pt 8pt;
    background: #f0f4f8;
    border-left: 3pt solid #0f3460;
}
.footer {
    margin-top: 24pt;
    padding-top: 8pt;
    border-top: 1px solid #ddd;
    font-size: 8pt;
    color: #999;
}
"""


CERTAINTY_LABELS = {
    "solid": "Solide",
    "to_confirm": "A confirmer",
    "unknown": "Inconnu",
    "blocking": "Bloquant",
}

MARKDOWN_EXTENSIONS = ["tables", "fenced_code", "nl2br", "sane_lists"]
SANITIZED_TAGS = sorted(
    set(bleach.sanitizer.ALLOWED_TAGS).union(
        {"p", "br", "hr", "pre", "h1", "h2", "h3", "table", "thead", "tbody", "tr", "th", "td"}
    )
)
SANITIZED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "a": ["href", "title", "rel", "target"],
    "th": ["colspan", "rowspan"],
    "td": ["colspan", "rowspan"],
}
SANITIZED_PROTOCOLS = ["http", "https", "mailto"]


def build_markdown(payload: RendererRequest) -> str:
    blocks: list[str] = [f"# {payload.title}"]
    if payload.quality_label:
        blocks.append(f"**Statut qualite** : {payload.quality_label}")
    blocks.append(payload.summary)
    for section in payload.sections:
        cert_label = CERTAINTY_LABELS.get(section.certainty, section.certainty)
        blocks.append(f"## {section.title}  [{cert_label}]")
        blocks.append(section.content)
    blocks.append("---")
    blocks.append("*Genere par Cadris*")
    return "\n\n".join(blocks)


def render_safe_markdown(content: str) -> str:
    html_content = md_lib.markdown(content, extensions=MARKDOWN_EXTENSIONS)
    return bleach.clean(
        html_content,
        tags=SANITIZED_TAGS,
        attributes=SANITIZED_ATTRIBUTES,
        protocols=SANITIZED_PROTOCOLS,
        strip=True,
    )


def build_html(payload: RendererRequest) -> str:
    safe_title = escape(payload.title)
    safe_summary = escape(payload.summary)
    parts: list[str] = [f"<h1>{safe_title}</h1>"]
    if payload.quality_label:
        parts.append(
            f'<p class="quality-label"><strong>Statut qualite</strong> : {escape(payload.quality_label)}</p>'
        )
    parts.append(f"<p>{safe_summary}</p>")
    for section in payload.sections:
        certainty_class = f"certainty-{section.certainty}"
        cert_label = CERTAINTY_LABELS.get(section.certainty, section.certainty)
        tag = f'<span class="certainty-tag {certainty_class}">{escape(cert_label)}</span>'
        parts.append(f"<h2>{escape(section.title)} {tag}</h2>")
        parts.append(render_safe_markdown(section.content))
    parts.append('<div class="footer">Genere par Cadris</div>')
    body = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><style>{CSS_TEMPLATE}</style></head>
<body>{body}</body>
</html>"""


@app.get("/health")
async def healthcheck():
    return {"ok": True}


@app.post("/internal/renderer/markdown", response_model=RendererResponse)
async def render_markdown(payload: RendererRequest):
    return RendererResponse(markdown=build_markdown(payload))


@app.post("/internal/renderer/html", response_model=HtmlResponse)
async def render_html(payload: RendererRequest):
    return HtmlResponse(html=build_html(payload))


@app.post("/internal/renderer/pdf")
async def render_pdf(payload: RendererRequest):
    from xhtml2pdf import pisa

    html_content = build_html(payload)
    buffer = io.BytesIO()
    try:
        pisa_status = pisa.CreatePDF(html_content, dest=buffer)
        if pisa_status.err:
            raise RuntimeError(f"xhtml2pdf reported {pisa_status.err} error(s)")
    except Exception:
        logger.exception("PDF generation failed for dossier '%s'", payload.title)
        return JSONResponse(
            status_code=503,
            content={
                "error": "pdf_generation_failed",
                "message": "La generation PDF a echoue. Le dossier reste disponible en markdown et HTML.",
            },
        )
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="dossier.pdf"'},
    )
