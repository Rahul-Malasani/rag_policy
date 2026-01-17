import json
import re
from pathlib import Path

# Paths
PAGES_PATH = Path("../data/processed/pages.json")
OUTPUT_DIR = Path("../data/processed")

# Regex patterns tailored for insurance policy PDFs
CLAUSE_HEADER_PATTERN = re.compile(r"^(\d+(\.\d+)+)\s+(.*)")
DEFINITION_PATTERN = re.compile(r"^(\d+\.\d+\.\d+)\.\s+(.*?)(?:means|refers to)\b", re.IGNORECASE)

def load_pages():
    with open(PAGES_PATH, "r") as f:
        return json.load(f)

def extract_clauses(pages):
    clauses = []
    current = None

    for page in pages:
        page_no = page["page_number"]
        lines = page["text"].split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = CLAUSE_HEADER_PATTERN.match(line)
            if match:
                if current:
                    clauses.append(current)

                clause_id = match.group(1)
                title = match.group(3)

                current = {
                    "clause": clause_id,
                    "title": title,
                    "content": "",
                    "page_start": page_no,
                    "page_end": page_no,
                    "type": "policy_clause"
                }
            elif current:
                current["content"] += line + " "
                current["page_end"] = page_no

    if current:
        clauses.append(current)

    return clauses

def extract_definitions(pages):
    definitions = []
    current = None

    for page in pages:
        page_no = page["page_number"]
        lines = page["text"].split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = DEFINITION_PATTERN.match(line)
            if match:
                if current:
                    definitions.append(current)

                current = {
                    "clause": match.group(1),
                    "term": match.group(2),
                    "definition": line,
                    "page": page_no,
                    "type": "definition"
                }
            elif current:
                current["definition"] += " " + line

    if current:
        definitions.append(current)

    return definitions

def save_json(data, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / filename, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    pages = load_pages()

    clauses = extract_clauses(pages)
    definitions = extract_definitions(pages)

    save_json(clauses, "clauses.json")
    save_json(definitions, "definitions.json")

    print(f"Extracted {len(clauses)} clauses")
    print(f"Extracted {len(definitions)} definitions")

'''clause aware structuring (option 3(see obsidian notes for reference)- section aware hierarchical representation)'''