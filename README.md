# Enterprise Document QA Assistant (RAG)

This project implements a **Retrieval-Augmented Generation (RAG)** system for querying enterprise documents with grounded answers and citations.

The goal is to build an end-to-end pipeline covering document ingestion, chunking, embeddings, retrieval, and answer generation.

---

## Progress (Day 1 – Day 3)

### Day 1 — Project Setup & Environment
- Created project repository structure and virtual environment
- Installed core dependencies for RAG (LangChain, sentence-transformers, PDF parsing, Streamlit)
- Defined configuration and requirements for scalable development
- Established clean GitHub repo structure with `.gitignore`

### Day 2 — Document Ingestion Pipeline
- Implemented document ingestion for **TXT / Markdown / PDF**
- Extracted text page-wise with metadata (`doc_id`, `page`, `source`)
- Handled real-world **Windows encoding issues** (UTF-16, UTF-8 BOM, null bytes)
- Normalized and cleaned text for downstream processing
- Stored processed output as `raw_pages.jsonl`

### Day 3 — Token-Aware Chunking
- Designed sentence-aware chunking strategy
- Implemented **token-based chunking with overlap** to preserve context
- Generated chunk-level metadata (`chunk_id`, `doc_id`, `page`)
- Produced `chunks.jsonl` ready for embeddings and retrieval
- Ensured clean, debuggable, and interview-ready pipeline

---

## Tech Stack
- Python 3
- LangChain
- Sentence-Transformers
- pdfplumber / PyMuPDF
- Streamlit
- Git & GitHub

---

## Next Steps
- Generate embeddings for document chunks
- Build vector index (FAISS / Chroma)
- Implement semantic retrieval
- Add LLM-based answer generation with citations
- Create Streamlit UI for interactive querying

### Day 4 — Embeddings Generation
- Implemented semantic embeddings using **sentence-transformers**
- Used `all-MiniLM-L6-v2` model for efficient and high-quality vector representations
- Generated normalized dense embeddings for each text chunk
- Stored embeddings separately from metadata for scalability and traceability
- Produced:
  - `embeddings.npy` — numeric vector representations
  - `embeddings_meta.jsonl` — chunk metadata for citation and retrieval

Key focus:
- Semantic similarity instead of keyword matching
- Vector normalization to enable cosine similarity search
- LLM-agnostic embedding pipeline design

---

### Day 5 — Vector Store & Semantic Retrieval
- Built a **FAISS-based vector index** for fast approximate nearest neighbor search
- Used `IndexFlatIP` with normalized embeddings for cosine similarity
- Implemented a retriever that:
  - Encodes user queries into vectors
  - Performs top-k semantic search
  - Returns relevant chunks with scores and metadata
- Added edge-case handling for small datasets (FAISS empty-slot filtering)
- Verified end-to-end semantic retrieval with real queries

Key focus:
- Efficient similarity search at scale
- Clean separation of embeddings, index, and metadata
- Production-style retrieval logic with robustness and explainability

