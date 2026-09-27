from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
Answer this student's question.

Question:
{question}

Requirements:
- Answer directly first.
- Use simple language.
- Add a short example when useful.
- If the question is ambiguous, state the assumption you made.
- Do not claim certainty for facts that are genuinely uncertain.
"""
    return generate_text(prompt)
