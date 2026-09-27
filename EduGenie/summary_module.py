from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the educational passage below for quick revision.

Passage:
{text}

Requirements:
- Preserve the important facts and relationships.
- Remove repetition and unnecessary detail.
- Use simple language.
- Return a short heading followed by 5-8 bullet points.
"""
    return generate_text(prompt)
