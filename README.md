# Enterprise Document QA Assistant (RAG System)

A production-style Retrieval-Augmented Generation (RAG) system for querying
enterprise documents using semantic search and large language models.
The system generates grounded answers strictly from retrieved documents,
with clear source citations.

---

## 🚀 Key Features
- Ingests enterprise documents (PDF, TXT, DOCX)
- Semantic chunking for long-form content
- Dense vector embeddings using Sentence Transformers
- FAISS-based approximate nearest neighbor search
- LLM-based answer generation (Gemini)
- Streamlit UI for interactive querying
- Source-aware responses with document provenance

---

## 🧠 System Architecture (High Level)

Documents
↓
Ingestion (PDF / TXT / DOCX)
↓
Semantic Chunking
↓
Vector Embeddings
↓
FAISS Vector Index
↓
Retriever
↓
LLM (Gemini)
↓
User Interface (Streamlit)


---

## 📁 Project Structure

docqa/
├── app/ # Streamlit application
├── src/ # Core pipeline modules
│ ├── ingest.py
│ ├── chunker.py
│ ├── embedder.py
│ ├── retriever.py
│ └── generator.py
├── data/ # Generated artifacts (ignored in Git)
├── requirements.txt
└── README.md


---

## ⚙️ Setup & Execution (Windows)

### Create virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Install dependencies
pip install -r requirements.txt
Run the pipeline
python src/ingest.py --input data/raw --out data/raw_pages.jsonl
python src/chunker.py
python src/embedder.py
python src/retriever.py
python -m streamlit run app/streamlit_app.py
Access the UI at:

http://localhost:8501
📊 Example Query
Question: What is the leave policy?

Behavior:

Answer generated only from retrieved document chunks

Includes document-level citations

Prevents hallucinations through retrieval grounding

🧪 Key Learnings
Designing effective chunking strategies for enterprise documents

Trade-offs between recall and precision in vector search

Preventing hallucinations using retrieval-grounded prompting

Structuring modular RAG pipelines for maintainability

Building end-to-end ML systems with clean backend separation

🔒 Notes
Environment variables are excluded from version control

Generated artifacts and indexes are ignored

Sample documents are non-sensitive, dummy enterprise data
