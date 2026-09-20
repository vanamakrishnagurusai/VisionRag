import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class RAGGenerator:

    def __init__(self, model="gemini-3.6-flash"):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set in the .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

    def generate_answer(self, query, retrieved_results):

        if not retrieved_results:
            return (
                "I could not find any relevant images "
                "for this query."
            )

        context_parts = []

        for result in retrieved_results:

            context_parts.append(
                f"""
Image: {result.get("filename")}

Similarity score:
{result.get("score")}

Caption:
{result.get("caption")}

Detected objects:
{result.get("objects")}

Visual context:
{result.get("multimodal_context")}
"""
            )

        context = "\n".join(context_parts)

        prompt = f"""
You are VisionRAG, a visual retrieval assistant.

Answer the user's question using ONLY the
retrieved visual evidence below.

Rules:
- Do not invent objects.
- Do not invent people or actions.
- Do not invent locations.
- Do not make claims unsupported by the evidence.
- If the evidence is insufficient, say so.
- Keep the answer concise.

User query:
{query}

Retrieved visual evidence:
{context}

Answer the user's query.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text