"""Extraction du texte depuis un CV (PDF ou DOCX)."""
import os
from pathlib import Path


def extract_text_from_pdf(file_path: str) -> str:
    """Extrait le texte d'un fichier PDF."""
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    reader = PdfReader(file_path)
    parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return "\n\n".join(parts).strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extrait le texte d'un fichier DOCX."""
    from docx import Document
    doc = Document(file_path)
    return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip()).strip()


def extract_text_from_cv(file_path: str) -> str:
    """
    Extrait le texte d'un CV (PDF ou DOCX).
    :param file_path: chemin vers le fichier
    :return: texte brut du CV
    :raises ValueError: si le format n'est pas supporté
    """
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(file_path)
    if suffix in (".docx", ".doc"):
        if suffix == ".doc":
            raise ValueError("Le format .doc n'est pas supporté. Veuillez utiliser un fichier .docx.")
        return extract_text_from_docx(file_path)
    raise ValueError(f"Format non supporté : {suffix}. Utilisez un fichier PDF ou DOCX.")
