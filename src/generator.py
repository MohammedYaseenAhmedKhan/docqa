# src/generator.py
import os
from typing import List, Dict
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def generate_answer(question: str, chunks: List[Dict]) -> str:
    """
    Generate an answer using Gemini based strictly on retrieved document chunks.
    """

    context = "\n\n".join(
        [f"Source ({c['doc_id']} page {c['page']}): {c['text']}" for c in chunks]
    )

    prompt = f"""
You are an enterprise document QA assistant.
Answer the question ONLY using the context below.
If the answer is not found in the context, say:
"Answer not found in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )

    return response.text.strip()
