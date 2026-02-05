import os
from typing import List, Dict
from google import genai


def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Please set it before running the application."
        )

    return genai.Client(api_key=api_key)


def build_prompt(question: str, chunks: List[Dict]) -> str:
    context = ""
    for i, chunk in enumerate(chunks, 1):
        context += (
            f"\nSource {i} ({chunk['doc_id']} - Page {chunk['page']}):\n"
            f"{chunk['text']}\n"
        )

    return f"""
You are an enterprise policy assistant.

Answer the question STRICTLY using the sources below.
If the answer is not present, say:
"The information is not available in the provided documents."

Question:
{question}

Sources:
{context}

Answer:
""".strip()


def generate_answer(question: str, chunks: List[Dict]) -> str:
    client = get_gemini_client()
    prompt = build_prompt(question, chunks)

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.2},
    )

    return response.text.strip()
