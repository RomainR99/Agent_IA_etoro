"""Export de la lettre de motivation en PDF et DOCX."""
import io
from pathlib import Path


def export_to_docx(text: str, output_path: str | None = None) -> bytes | str:
    """
    Exporte le texte en fichier Word (.docx).
    :param text: contenu de la lettre
    :param output_path: si fourni, enregistre le fichier et retourne le chemin
    :return: bytes du fichier si output_path est None, sinon output_path
    """
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    for paragraph in text.split("\n\n"):
        p = doc.add_paragraph(paragraph)
        p.paragraph_format.space_after = Pt(6)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    data = buffer.getvalue()
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(data)
        return output_path
    return data


def export_to_pdf(text: str, output_path: str | None = None) -> bytes | str:
    """
    Exporte le texte en PDF.
    :param text: contenu de la lettre
    :param output_path: si fourni, enregistre le fichier et retourne le chemin
    :return: bytes du fichier si output_path est None, sinon output_path
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    import html
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        spaceAfter=8,
    )
    story = []
    for block in text.split("\n\n"):
        if block.strip():
            safe = html.escape(block).replace("\n", "<br/>")
            story.append(Paragraph(safe, body_style))
    doc.build(story)
    buffer.seek(0)
    data = buffer.getvalue()
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(data)
        return output_path
    return data
