# parser.py
# This file reads PDF and DOCX files and extracts all text

import pdfplumber
from docx import Document

def extract_text_from_pdf(file_path):
    """
    Opens a PDF file and reads all text from it.
    
    Args:
        file_path: The path to your PDF file (like "sample_resume.pdf")
    
    Returns:
        All the text from the PDF as one big string
    """
    text = ""
    
    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        # Go through each page
        for page in pdf.pages:
            # Extract text from this page and add it
            text += page.extract_text() + "\n"
    
    return text


def extract_text_from_docx(file_path):
    """
    Opens a Word document and reads all text from it.
    
    Args:
        file_path: The path to your DOCX file
    
    Returns:
        All the text from the document
    """
    doc = Document(file_path)
    text = ""
    
    # Go through each paragraph in the document
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    return text


def extract_text(file_path):
    """
    Smart function that detects if the file is PDF or DOCX
    and calls the correct function.
    
    Args:
        file_path: Path to the resume file
    
    Returns:
        All text from the file
    """
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return "ERROR: File must be .pdf or .docx"


# Test code - runs when you execute this file directly
if __name__ == "__main__":
    print("Reading resume...")
    result = extract_text("sample_resume.docx")  # ← CHANGED FROM .pdf TO .docx
    print("\n--- RESUME TEXT ---\n")
    print(result)
    print("\n--- END OF RESUME ---")
