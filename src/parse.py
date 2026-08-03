import fitz  # PyMuPDF
import json
import re
from pathlib import Path

METADATA_PATH = Path("data/metadata.json")
CHUNKS_PATH = Path("data/chunks.json")

CHUNK_SIZE = 500       # target words per chunk
CHUNK_OVERLAP = 50     # words of overlap between consecutive chunks

SECTION_PATTERNS = [
    r"^(\d+\.?\s*)?abstract$",
    r"^(\d+\.?\s*)?introduction$",
    r"^(\d+\.?\s*)?related work$",
    r"^(\d+\.?\s*)?background$",
    r"^(\d+\.?\s*)?method(ology)?$",
    r"^(\d+\.?\s*)?approach$",
    r"^(\d+\.?\s*)?experiment(s)?$",
    r"^(\d+\.?\s*)?result(s)?$",
    r"^(\d+\.?\s*)?discussion$",
    r"^(\d+\.?\s*)?conclusion(s)?$",
    r"^(\d+\.?\s*)?references$",
]
SECTION_REGEX = re.compile("|".join(SECTION_PATTERNS), re.IGNORECASE)


def extract_text_with_sections(pdf_path):
    doc = fitz.open(pdf_path)
    current_section = "unknown"
    sections = []

    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if not text:
                continue

            first_line = text.split("\n")[0].strip().lower()
            if len(first_line) < 40 and SECTION_REGEX.match(first_line):
                # Strip leading numbering (e.g. "2. related work" -> "related work")
                normalized = re.sub(r"^\d+\.?\s*", "", first_line).strip()
                current_section = normalized
                continue

            sections.append((current_section, text))

    doc.close()
    return sections


def chunk_text(sections, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    section_order = []
    merged = {}
    for section, text in sections:
        if section not in merged:
            merged[section] = []
            section_order.append(section)
        merged[section].append(text)

    chunks = []
    for section in section_order:
        full_text = " ".join(merged[section])
        words = full_text.split()
        if not words:
            continue

        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_str = " ".join(chunk_words)

            if len(chunk_str.strip()) > 0:
                chunks.append({
                    "section": section,
                    "text": chunk_str,
                })

            if end >= len(words):
                break
            start = end - overlap

    return chunks


def process_all_papers():
    with open(METADATA_PATH) as f:
        papers = json.load(f)

    all_chunks = []
    failed = []

    for paper in papers:
        pdf_path = Path(paper["pdf_path"])
        if not pdf_path.exists():
            failed.append(paper["id"])
            continue

        try:
            sections = extract_text_with_sections(pdf_path)
            paper_chunks = chunk_text(sections)

            for i, chunk in enumerate(paper_chunks):
                all_chunks.append({
                    "chunk_id": f"{paper['id']}_chunk{i}",
                    "paper_id": paper["id"],
                    "title": paper["title"],
                    "section": chunk["section"],
                    "text": chunk["text"],
                })

        except Exception as e:
            print(f"Failed to parse {paper['id']}: {e}")
            failed.append(paper["id"])

    with open(CHUNKS_PATH, "w") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"\nDone. {len(all_chunks)} chunks created from {len(papers) - len(failed)} papers.")
    if failed:
        print(f"Failed to parse {len(failed)} papers: {failed}")
    print(f"Chunks saved to {CHUNKS_PATH}")

    return all_chunks


if __name__ == "__main__":
    process_all_papers()