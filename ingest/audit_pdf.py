# ingest/audit_pdf.py
import fitz

def audit_pdf(path):
    doc = fitz.open(path)

    print("=" * 80)
    print(f"Auditing PDF: {path}")
    print("=" * 80)

    for i, page in enumerate(doc):
        page_number = i + 1

        # ---- Existing checks (KEEP THESE) ----
        raw_text = page.get_text()
        has_text = bool(raw_text.strip())
        images = page.get_images(full=True)
        num_images = len(images)

        # ---- NEW: block-level inspection ----
        blocks = page.get_text("blocks")
        text_blocks = [b for b in blocks if b[6] == 0]   # block type 0 = text
        image_blocks = [b for b in blocks if b[6] == 1]  # block type 1 = image

        num_text_blocks = len(text_blocks)
        num_image_blocks = len(image_blocks)

        # ---- NEW: text density heuristic ----
        text_length = len(raw_text)
        page_area = page.rect.width * page.rect.height
        text_density = round(text_length / page_area, 6) if page_area else 0

        # ---- Heuristic flags (decision aids) ----
        flags = []

        if not has_text:
            flags.append("NO_TEXT_LAYER")

        if has_text and text_density < 0.0005:
            flags.append("LOW_TEXT_DENSITY")

        if num_image_blocks > num_text_blocks:
            flags.append("IMAGE_HEAVY")

        if num_text_blocks > 50:
            flags.append("MANY_TEXT_BLOCKS (possible table or layout noise)")

        # ---- Output (human-readable, grep-friendly) ----
        print(
            f"Page {page_number:02d} | "
            f"text={'YES' if has_text else 'NO'} | "
            f"text_blocks={num_text_blocks:02d} | "
            f"image_blocks={num_image_blocks:02d} | "
            f"density={text_density:.6f} | "
            f"flags={flags}"

        )

    print("=" * 80)

if __name__ == "__main__":
    pdf_path = "data/raw/policy.pdf"
    audit_pdf(pdf_path)

  

