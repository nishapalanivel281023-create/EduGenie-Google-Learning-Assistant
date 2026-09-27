import os
from functools import lru_cache
from google import genai
from google.genai import types


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini cannot be configured."""


@lru_cache(maxsize=1)
def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is missing. Add it to the .env file."
        )
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, *, temperature: float = 0.3) -> str:
    client = get_client()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=(
                "You are EduGenie, a friendly educational assistant. "
                "Give accurate, age-appropriate, concise educational help. "
                "Explain unfamiliar terms and do not invent sources."
            ),
        ),
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def generate_json(prompt: str, schema: dict):
    client = get_client()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
            response_schema=schema,
            system_instruction=(
                "You are EduGenie. Return only data matching the requested schema. "
                "Create educational content that is clear, accurate, and concise."
            ),
        ),
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned empty JSON output.")
    return text.strip()
