# Enterprise Document QA Assistant (RAG System)

A Retrieval-Augmented Generation (RAG) system that ingests enterprise documents,
performs semantic search using vector embeddings, and generates grounded answers
with citations using an LLM.

---

## 🚀 Features

- Ingests **PDF, TXT, DOCX** enterprise documents
- Intelligent **chunking** for long documents
- **Sentence-Transformers embeddings**
- **FAISS** vector similarity search
- **Gemini LLM** for answer generation
- **Streamlit UI** for interactive Q&A
- Clear document **citations and provenance**

---

## 🧠 Architecture (High Level)

Documents
↓
Ingestion (PDF/TXT/DOCX)
↓
Chunking
↓
Embeddings
↓
FAISS Vector Index
↓
Retriever
↓
LLM (Gemini)
↓
Streamlit UI


---

## 📁 Project Structure

docqa/
├── app/
│ └── streamlit_app.py
├── data/
│ ├── raw/ # Original documents
│ ├── raw_pages.jsonl # Ingested pages
│ ├── chunks.jsonl # Chunked text
│ ├── embeddings.npy
│ ├── embeddings_meta.jsonl
│ └── faiss.index
├── src/
│ ├── ingest.py
│ ├── chunker.py
│ ├── embedder.py
│ ├── retriever.py
│ └── generator.py
├── requirements.txt
├── README.md


---

## ⚙️ Setup Instructions (Windows)

### 1️⃣ Create Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
2️⃣ Install Dependencies
pip install -r requirements.txt
▶️ Run the Full Pipeline
Step 1: Ingest Documents
python src/ingest.py --input data/raw --out data/raw_pages.jsonl
Step 2: Chunk Documents
python src/chunker.py
Step 3: Generate Embeddings + FAISS Index
python src/embedder.py
Step 4: Test Retrieval
python src/retriever.py
Step 5: Run Streamlit UI
python -m streamlit run app/streamlit_app.py
Open browser:

http://localhost:8501
📊 Example Question
What is the leave policy?

✔️ Answer generated only from retrieved documents
✔️ Includes citations

🧪 Key Concepts Used
Retrieval-Augmented Generation (RAG)

Dense Vector Search

Cosine Similarity

FAISS ANN Indexing

Prompt Grounding

Hallucination Control

Enterprise Compliance

🧩 Day-wise Progress
Day 1–3: Setup, ingestion, chunking

Day 4–5: Embeddings + FAISS retrieval

Day 6: Gemini-based generation

Day 7: Streamlit UI

Day 8+: Documentation, cleanup, evaluation

🔒 Notes
.env is excluded from Git

Generated artifacts are ignored

Documents are dummy enterprise data

