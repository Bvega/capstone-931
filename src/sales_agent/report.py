from __future__ import annotations

from datetime import date
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from sales_agent.pipeline import PipelineResult


def make_markdown_report(account: dict, result: PipelineResult, run_date: str, model: str) -> str:
    sources = "\n".join(f"- [{source.title}]({source.url})" for source in result.sources)
    return f"""# Sales Account Brief: {account['company_name']}

**Research date:** {run_date}  
**Product:** {account['product_name']} ({account['product_category']})  
**Model:** {model}

{result.brief_markdown}

## Sources

{sources or 'No source annotations were returned; verify the research before use.'}
"""


def make_pdf_report(account: dict, result: PipelineResult, run_date: str, model: str) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.48 * inch,
        bottomMargin=0.45 * inch,
        title=f"Sales Account Brief - {account['company_name']}",
        author="CAP 931 Sales Agent Prototype",
    )
    base = getSampleStyleSheet()
    title = ParagraphStyle("BriefTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=16, leading=18, spaceAfter=5, textColor="#15263D", alignment=0)
    meta = ParagraphStyle("BriefMeta", parent=base["Normal"], fontName="Helvetica", fontSize=8, leading=10, textColor="#46566B", spaceAfter=3)
    body = ParagraphStyle("BriefBody", parent=base["BodyText"], fontName="Helvetica", fontSize=8, leading=10.2, spaceAfter=3)
    heading = ParagraphStyle("BriefHeading", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=12, spaceBefore=4, spaceAfter=2, textColor="#15263D")
    story = [
        Paragraph(f"Sales Account Brief: {escape(account['company_name'])}", title),
        Paragraph(
            f"Research date: {escape(run_date)} &nbsp; | &nbsp; Product: {escape(account['product_name'])} ({escape(account['product_category'])}) &nbsp; | &nbsp; Model: {escape(model)}",
            meta,
        ),
        Paragraph(f"Company: {escape(account['company_url'])}", meta),
        Spacer(1, 3),
    ]
    for raw_line in result.brief_markdown.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("### ") or line.startswith("## ") or line.startswith("# "):
            story.append(Paragraph(escape(line.lstrip("# ")), heading))
        else:
            # Keep source links visible in the compact PDF as plain URLs.
            line = line.replace("**", "")
            import re

            line = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 (\2)", line)
            story.append(Paragraph(escape(line), body))
    if result.sources:
        story.append(Paragraph("Sources", heading))
        for source in result.sources[:8]:
            story.append(Paragraph(f"{escape(source.title)}: {escape(source.url)}", body))
    document.build(story)
    return buffer.getvalue()

