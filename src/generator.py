# src/generator.py
import os
from typing import List, Dict
from google import genai

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """
You are an enterprise document assistant.

Rules:
- Use ONLY the provided document sources
- Do NOT use external knowledge
- If the answer is not present, say:
  "I don't know based on the provided documents"
- Provide a clear, structured answer
- Cite sources inline using [doc_id:page]
"""

def format_sources(chunks: List[Dict]) -> str:
    formatted = []
    for i, c in enumerate(chunks, 1):
        block = (
            f"Source {i}\n"
            f"Document: {c['doc_id']}\n"
            f"Page: {c['page']}\n"
            f"Content:\n{c['text']}\n"
        )
        formatted.append(block)
    return "\n---\n".join(formatted)

def generate_answer(question: str, chunks: List[Dict]) -> str:
    sources_text = format_sources(chunks)

    prompt = f"""
{SYSTEM_INSTRUCTION}

SOURCES:
{sources_text}

QUESTION:
{question}

INSTRUCTIONS:
- Combine information from relevant sources
- Keep the answer concise but complete
- Add citations after each factual statement
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0.2,
            "max_output_tokens": 400
        }
    )

    return response.text.strip()

if __name__ == "__main__":
    from retriever import Retriever

    retriever = Retriever()
    chunks = retriever.search("What is the leave policy?", k=5)

    answer = generate_answer(
        "What is the leave policy?",
        chunks
    )

    print("\nFINAL ANSWER:\n")
    print(answer)