
# ResearchGPT — Evaluated RAG Assistant for Scientific Papers

A retrieval-augmented generation (RAG) system for querying scientific papers (arXiv cs.AI/cs.LG),
built with a focus on **rigorous evaluation and production-grade MLOps** rather than just a demo chatbot.

## Highlights
- **Hybrid retrieval**: BM25 + dense embeddings, reranked with a cross-encoder
- **LoRA/QLoRA fine-tuning** on self-instruct Q&A pairs to reduce hallucination and enforce citation format
- **Automated evaluation harness**: faithfulness, context precision/recall, and citation accuracy scored against a hand-labeled gold set
- **CI/CD gating**: GitHub Actions runs the eval suite on every change, failing the build if retrieval quality regresses
- **Full MLOps stack**: MLflow experiment tracking, Docker containerization, FastAPI backend

## Status
 In progress — Week 1 (data + retrieval) underway

- [x] **Day 1**: arXiv ingestion pipeline — fetches paper metadata and PDFs via the arXiv API
- [x] **Day 2**: PDF parsing + chunking — extracts text, tags it by section (abstract/method/results/etc.), and splits it into overlapping ~500-word chunks
- [ ] Day 3: Embeddings + FAISS vector index
- [ ] Day 4: Basic dense retrieval
- [ ] Day 5: Hybrid search (BM25 + dense)
- [ ] Day 6: FastAPI skeleton
- [ ] Week 2: LLM generation + LoRA fine-tuning
- [ ] Week 3: Evaluation harness + MLOps + deployment

## Progress so far
- Ingested **30 papers** from arXiv (`cs.AI` / `cs.LG`)
- Parsed and chunked into **~800 text chunks**, tagged by section
- Known limitation: section-tagging accuracy is reduced on two-column PDF layouts, since PyMuPDF's block extraction order doesn't always follow true reading order across columns. Chunk *text* is unaffected — only the section *label* metadata is occasionally imprecise. A future improvement would be swapping in GROBID for structure-aware parsing.

## Project Structure
researchgpt/
├── data/
│ ├── raw_pdfs/ # downloaded arXiv PDFs
│ ├── metadata.json # paper metadata (title, authors, abstract, etc.)
│ └── chunks.json # parsed + chunked paper text, tagged by section
├── src/
│ ├── ingest.py # arXiv fetching + PDF download
│ ├── parse.py # PDF text extraction + chunking
│ ├── retrieval.py # (in progress) embeddings + search
│ └── api.py # (planned) FastAPI backend
├── requirements.txt
└── README.md

## Setup

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Usage

**1. Fetch papers from arXiv**
```bash
python src/ingest.py
```

**2. Parse and chunk PDFs**
```bash
python src/parse.py
```

## Tech Stack
Python · PyMuPDF · arXiv API · LangChain (planned) · FAISS (planned) · Hugging Face Transformers (planned) · PEFT/LoRA (planned) · FastAPI (planned) · Docker (planned) · MLflow (planned) · GitHub Actions (planned)