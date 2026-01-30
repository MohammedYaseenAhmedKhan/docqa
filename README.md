📘 Enterprise Document QA Assistant (RAG System)

A production-style Retrieval-Augmented Generation (RAG) system that ingests enterprise documents, performs semantic search using vector embeddings, and generates grounded answers with citations using Google Gemini.

🎯 Objective

Enable employees to ask natural-language questions over internal company documents (HR policies, benefits, IT security, onboarding) and receive accurate, source-backed answers.

🧠 Core Concepts Used

Retrieval-Augmented Generation (RAG)

Dense vector embeddings

FAISS similarity search

Context-aware chunking

LLM grounding & hallucination control

Enterprise document provenance

🏗️ Architecture
Documents (PDF / TXT / MD)
        ↓
Ingestion & Cleaning
        ↓
Chunking (overlap-aware)
        ↓
Embeddings (Sentence Transformers)
        ↓
FAISS Vector Index
        ↓
Retriever (Top-k semantic search)
        ↓
LLM (Gemini 2.5 Flash)
        ↓
Answer + Source Context

📂 Project Structure
docqa/
├── data/
│   ├── raw/                # Source documents
│   ├── raw_pages.jsonl     # Page-level extracted text
│   └── chunks.jsonl        # Chunked passages
├── src/
│   ├── ingest.py           # Document ingestion
│   ├── chunker.py          # Text chunking
│   ├── embedder.py         # Embedding generation
│   ├── indexer.py          # FAISS index build/load
│   ├── retriever.py        # Semantic retrieval
│   └── generator.py        # Gemini-based answer generation
├── notebooks/
├── tests/
├── README.md
└── requirements.txt

🗓️ Implementation Timeline
✅ Day 1 — Environment & Repo Setup

Virtual environment setup (Windows)

Project structure & Git initialization

Dependency management

✅ Day 2 — Document Ingestion

Supported formats: .txt, .pdf (OCR-ready)

Metadata preserved: doc_id, page, source

Output: raw_pages.jsonl

✅ Day 3 — Chunking & Text Cleaning

Fixed encoding issues (BOM, null chars)

Chunk size: ~300–500 tokens

Overlap for context continuity

Output: chunks.jsonl

✅ Day 4 — Embeddings

Model: all-MiniLM-L6-v2

Normalized dense vectors

Batched embedding generation

Stored alongside chunk metadata

✅ Day 5 — Vector Search (FAISS)

Index type: IndexFlatIP (cosine similarity)

Persisted FAISS index

Top-k semantic retrieval with scores

✅ Day 6 — Answer Generation (Gemini)

LLM: Gemini 2.5 Flash

Prompt grounded strictly in retrieved chunks

Hallucination control via instructions

End-to-end RAG working locally
