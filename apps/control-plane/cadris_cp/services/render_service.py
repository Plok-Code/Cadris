"""Markdown → HTML / PDF rendering helpers."""
from __future__ import annotations

import io
from html import escape

import bleach
import markdown as md_lib

_MARKDOWN_EXTENSIONS = ["tables", "fenced_code", "nl2br", "sane_lists"]
_SANITIZED_TAGS = sorted(
    set(bleach.sanitizer.ALLOWED_TAGS).union(
        {"p", "br", "hr", "pre", "h1", "h2", "h3", "table", "thead", "tbody", "tr", "th", "td"}
    )
)
_SANITIZED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "a": ["href", "title", "rel", "target"],
    "th": ["colspan", "rowspan"],
    "td": ["colspan", "rowspan"],
}
_SANITIZED_PROTOCOLS = ["http", "https", "mailto"]

_PDF_CSS = """
@page { size: A4; margin: 2cm; }
body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #1a1a2e;
}
h1 { font-size: 18pt; color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 6pt; margin-bottom: 12pt; }
h2 { font-size: 13pt; color: #0f3460; margin-top: 16pt; margin-bottom: 6pt; }
h3 { font-size: 11pt; color: #16213e; margin-top: 12pt; margin-bottom: 4pt; }
p { margin-bottom: 8pt; }
ul, ol { margin-bottom: 8pt; padding-left: 20pt; }
li { margin-bottom: 3pt; }
table { width: 100%; border-collapse: collapse; margin-bottom: 10pt; font-size: 9pt; }
th, td { border: 1px solid #ccc; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #f0f4f8; font-weight: bold; color: #0f3460; }
code { font-family: Courier; font-size: 8pt; background: #f0f4f8; padding: 1pt 3pt; }
pre { background: #f0f4f8; padding: 6pt 10pt; font-size: 8pt; margin-bottom: 8pt; }
pre code { background: none; padding: 0; }
blockquote { border-left: 3pt solid #0f3460; margin: 8pt 0; padding: 4pt 10pt; color: #555; background: #f8f9fa; }
.footer { margin-top: 20pt; padding-top: 6pt; border-top: 1px solid #ddd; font-size: 7pt; color: #999; }
"""


def render_safe_markdown_html(content: str) -> str:
    html_content = md_lib.markdown(content, extensions=_MARKDOWN_EXTENSIONS)
    return bleach.clean(
        html_content,
        tags=_SANITIZED_TAGS,
        attributes=_SANITIZED_ATTRIBUTES,
        protocols=_SANITIZED_PROTOCOLS,
        strip=True,
    )


def md_to_pdf_bytes(title: str, content: str) -> bytes:
    """Convert a markdown document to PDF via HTML (supports tables, accents, formatting)."""
    from xhtml2pdf import pisa

    html_body = render_safe_markdown_html(content)
    safe_title = escape(title)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><style>{_PDF_CSS}</style></head>
<body>
<h1>{safe_title}</h1>
{html_body}
<div class="footer">Genere par Cadris</div>
</body>
</html>"""

    buffer = io.BytesIO()
    pisa.CreatePDF(html, dest=buffer)
    buffer.seek(0)
    return buffer.getvalue()
