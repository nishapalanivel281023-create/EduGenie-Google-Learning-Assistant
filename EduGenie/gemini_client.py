import os
import time
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
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=(
            "You are EduGenie, a friendly educational assistant. "
            "Give accurate, age-appropriate, concise educational help. "
            "Explain unfamiliar terms and do not invent sources."
        ),
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            text = getattr(response, "text", None)
            if not text:
                raise RuntimeError("Gemini returned an empty response.")
            return text.strip()
        except Exception as e:
            # 503 UNAVAILABLE or temporary spike vandha 2 seconds wait panni retry pannum
            if ("503" in str(e) or "UNAVAILABLE" in str(e)) and attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise e


def generate_json(prompt: str, schema: dict):
    client = get_client()
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    
    config = types.GenerateContentConfig(
        temperature=0.2,
        response_mime_type="application/json",
        response_schema=schema,
        system_instruction=(
            "You are EduGenie. Return only data matching the requested schema. "
            "Create educational content that is clear, accurate, and concise."
        ),
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            text = getattr(response, "text", None)
            if not text:
                raise RuntimeError("Gemini returned empty JSON output.")
            return text.strip()
        except Exception as e:
            if ("503" in str(e) or "UNAVAILABLE" in str(e)) and attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise e
