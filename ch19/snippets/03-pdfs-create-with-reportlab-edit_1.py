from pathlib import Path
from pypdf import PdfReader, PdfWriter

def merge(files, out):
    w = PdfWriter()
    for f in files:
        for page in PdfReader(f).pages:
            w.add_page(page)
    with open(out, "wb") as fh:
        w.write(fh)

def split(path, folder):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    for i, page in enumerate(PdfReader(path).pages, start=1):
        w = PdfWriter()
        w.add_page(page)
        with open(folder / f"page_{i:03d}.pdf", "wb") as fh:
            w.write(fh)

def search(path, word):
    """Page numbers containing word (text PDFs only; scans need OCR)."""
    return [i for i, page in enumerate(PdfReader(path).pages, start=1)
            if word.lower() in (page.extract_text() or "").lower()]
