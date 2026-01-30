📄 Enterprise Document Q&A Assistant (RAG-based)

An end-to-end Enterprise Document Question Answering System built using Retrieval-Augmented Generation (RAG).
This application allows users to query internal company documents using natural language and receive accurate, context-grounded answers through an interactive Streamlit UI.

🚀 Key Features

📂 Ingest enterprise documents (TXT, PDF-ready)

✂️ Semantic text chunking

🧠 Dense embeddings using SentenceTransformers

⚡ FAISS-based vector similarity search

🤖 Gemini LLM for answer generation

🖥️ Streamlit-based interactive UI

📌 Source-aware answers (document & page reference)

🏗️ Architecture Overview (RAG Pipeline)
Raw Documents
      ↓
Document Ingestion & Cleaning
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
FAISS Vector Index
      ↓
Retriever (Top-K relevant chunks)
      ↓
LLM (Gemini)
      ↓
Final Answer (Streamlit UI)

🧰 Tech Stack
Layer	Technology
Language	Python
Embeddings	sentence-transformers
Vector Store	FAISS
LLM	Google Gemini
UI	Streamlit
Parsing	pdfplumber
Env Mgmt	python-dotenv
📁 Project Structure
docqa/
├── app/
│   └── streamlit_app.py        # Streamlit UI
├── src/
│   ├── ingest.py               # Document ingestion
│   ├── chunker.py              # Text chunking
│   ├── embedder.py             # Embedding generation
│   ├── indexer.py              # FAISS indexing
│   ├── retriever.py            # Semantic retrieval
│   └── generator.py            # Gemini answer generation
├── data/
│   ├── raw/                    # Input documents
│   ├── processed/
│   ├── faiss.index
│   ├── embeddings_meta.jsonl
│   └── raw_pages.jsonl
├── requirements.txt
├── README.md
└── .env

⚙️ Setup Instructions (Windows)
1️⃣ Clone Repository
git clone https://github.com/MohammedYaseenAhmedKhan/docqa.git
cd docqa

2️⃣ Create & Activate Virtual Environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

3️⃣ Install Dependencies
pip install -r requirements.txt

🔑 Environment Configuration

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

📥 Add Documents

Place enterprise documents inside:

data/raw/


Example documents:

employee_handbook.txt

benefits_policy.txt

it_security_policy.txt

onboarding_guide.txt

🔄 Run the Data Pipeline

Run the following commands whenever documents are added or updated:

python src/ingest.py --input data/raw --out data/raw_pages.jsonl
python src/chunker.py
python src/embedder.py
python src/indexer.py

🖥️ Run the Streamlit Application
python -m streamlit run app/streamlit_app.py


Open in browser:

http://localhost:8501

💬 Example Queries

What is the leave policy?

What benefits are offered to employees?

What is the attendance policy?

What is the company code of conduct?

The system retrieves the most relevant document chunks and generates grounded answers using Gemini.

🧠 Why Retrieval-Augmented Generation (RAG)?

RAG improves reliability by:

Preventing hallucinations

Using only enterprise-approved documents

Providing explainable, source-backed answers

This makes the system suitable for internal company knowledge bases.

🛠️ Day-wise Development Breakdown
Day 1

Project setup and repository initialization

Virtual environment configuration

Folder structure creation

Dependency installation

Day 2

Document ingestion pipeline

Text extraction from raw files

JSONL page-wise storage

Day 3

Text chunking logic

Chunk size and overlap handling

Validation of chunk outputs

Day 4

Embedding generation using SentenceTransformers

Metadata creation

Storage of embeddings and references

Day 5

FAISS index creation

Semantic search implementation

Retriever validation with sample queries

Day 6

Gemini LLM integration

Answer generation using retrieved context

Streamlit UI development

End-to-end pipeline testing

README finalization and GitHub cleanup