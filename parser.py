import pdfplumber
from docx import Document

def extract_text(file_path: str, filename: str) -> str:
    if filename.endswith(".pdf"):
        return extract_from_pdf(file_path)
    elif filename.endswith(".docx"):
        return extract_from_docx(file_path)
    else:
        return ""

def extract_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])