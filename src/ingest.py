import arxiv
import json
import requests
from pathlib import Path
from tqdm import tqdm

RAW_PDF_DIR = Path("data/raw_pdfs")
METADATA_PATH = Path("data/metadata.json")

def fetch_papers(query="cat:cs.AI OR cat:cs.LG", max_results=500):
    RAW_PDF_DIR.mkdir(parents=True, exist_ok=True)

    client = arxiv.Client(page_size=100, delay_seconds=3, num_retries=3)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    metadata = []
    results = client.results(search)

    for result in tqdm(results, total=max_results, desc="Fetching papers"):
        paper_id = result.get_short_id()
        pdf_path = RAW_PDF_DIR / f"{paper_id}.pdf"

        if not pdf_path.exists():
            try:
                response = requests.get(result.pdf_url, timeout=30)
                response.raise_for_status()
                with open(pdf_path, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                print(f"Failed to download {paper_id}: {e}")
                continue

        metadata.append({
            "id": paper_id,
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "abstract": result.summary,
            "published": str(result.published),
            "categories": result.categories,
            "pdf_path": str(pdf_path),
        })

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nDone. {len(metadata)} papers saved. Metadata at {METADATA_PATH}")
    return metadata


if __name__ == "__main__":
    fetch_papers(query="cat:cs.AI OR cat:cs.LG", max_results=30)