"""
File parser for different document formats (txt, pdf, docx)
"""
import os
from typing import Union
import PyPDF2
from docx import Document


def parse_txt(file_path: str) -> str:
    """Parse text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Error parsing TXT file: {str(e)}")


def parse_pdf(file_path: str) -> str:
    """Parse PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error parsing PDF file: {str(e)}")


def parse_docx(file_path: str) -> str:
    """Parse DOCX file"""
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Error parsing DOCX file: {str(e)}")


def parse_file(file_path: str) -> str:
    """
    Parse file based on extension
    Supports: .txt, .pdf, .docx
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == '.txt':
        return parse_txt(file_path)
    elif ext == '.pdf':
        return parse_pdf(file_path)
    elif ext == '.docx':
        return parse_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats: .txt, .pdf, .docx")
