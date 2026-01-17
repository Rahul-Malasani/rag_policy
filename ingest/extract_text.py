import fitz  # PyMuPDF
from pathlib import Path
import json

PDF_PATH = Path("../data/raw/policy.pdf")
OUTPUT_PATH = Path("../data/processed/pages.json")

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        pages.append({
            "page_number": i + 1,
            "text": page.get_text("text").strip()
        })

    return pages

if __name__ == "__main__":
    pages = extract_pages(PDF_PATH)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(pages, f, indent=2)

    print(f"Extracted {len(pages)} pages → {OUTPUT_PATH}")
