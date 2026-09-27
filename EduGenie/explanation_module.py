import os
from functools import lru_cache

from gemini_client import generate_text


@lru_cache(maxsize=1)
def _load_local_pipeline():
    """
    Optional local LaMini-Flan-T5 implementation from the project specification.
    It is loaded only when USE_LOCAL_EXPLAINER=true.
    """
    from transformers import pipeline

    model_name = os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline(
        "text2text-generation",
        model=model_name,
        tokenizer=model_name,
    )


def explain_topic(topic: str) -> str:
    use_local = os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true"

    if use_local:
        try:
            pipe = _load_local_pipeline()
            prompt = (
                "Explain the following topic for a beginner in simple language. "
                "Use a short definition, key points, and one example: "
                f"{topic}"
            )
            result = pipe(prompt, max_new_tokens=220, do_sample=False)
            return result[0]["generated_text"].strip()
        except Exception:
            # Gemini remains the reliable fallback if the local model is unavailable.
            pass

    prompt = f"""
Explain the topic below to a beginner.

Topic:
{topic}

Format:
1. Simple definition
2. How it works / main idea
3. 3-5 key points
4. One easy example
5. One-line recap

Keep the explanation concise and easy to revise.
"""
    return generate_text(prompt)
