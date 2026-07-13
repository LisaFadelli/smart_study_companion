# PDF EXTRACTION

"""
No OCR, no Image Handling, just a page-aware output using PDF reader function
https://www.geeksforgeeks.org/python/extract-text-from-pdf-file-using-python/
"""

# importing required modules
from pypdf import PdfReader
from pathlib import Path

def extract_pages(pdf_path):
    pdf_path=Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    reader=PdfReader(str(pdf_path))
    pages=[]
    for i, page in enumerate(reader.pages, start =1):
        text=page.extract_text() or ""
        pages.append({"page":i, "text":text, "source":pdf_path.name})
    return pages

# if __name__ == "__main__":
#     pages = extract_pages("InformationRetrieval.pdf")   # <-- replace with a real PDF path
#     print(f"{len(pages)} pages extracted")
#     print(pages[0])