from __future__ import annotations

import io
import markdown as md_lib
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


class DossierSection(BaseModel):
    id: str
    title: str
    content: str
    certainty: str


class RendererRequest(BaseModel):
    title: str
    summary: str
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
p {
    margin-bottom: 10pt;
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
.footer {
    margin-top: 24pt;
    padding-top: 8pt;
    border-top: 1px solid #ddd;
    font-size: 8pt;
    color: #999;
}
"""


def build_markdown(payload: RendererRequest) -> str:
    blocks: list[str] = [f"# {payload.title}", payload.summary]
    for section in payload.sections:
        blocks.append(f"## {section.title}")
        blocks.append(section.content)
    return "\n\n".join(blocks)


def build_html(payload: RendererRequest) -> str:
    parts: list[str] = [f"<h1>{payload.title}</h1>", f"<p>{payload.summary}</p>"]
    for section in payload.sections:
        certainty_class = f"certainty-{section.certainty}"
        tag = f'<span class="certainty-tag {certainty_class}">{section.certainty}</span>'
        parts.append(f"<h2>{section.title} {tag}</h2>")
        html_content = md_lib.markdown(section.content)
        parts.append(html_content)
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
    pisa.CreatePDF(html_content, dest=buffer)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="dossier.pdf"'},
    )
