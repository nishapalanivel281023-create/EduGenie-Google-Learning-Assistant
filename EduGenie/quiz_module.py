import json
from pydantic import BaseModel, Field
from gemini_client import generate_json


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: int = Field(ge=0, le=3)
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {
                        "type": "array",
                        "minItems": 4,
                        "maxItems": 4,
                        "items": {"type": "string"},
                    },
                    "correct_answer": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 3,
                    },
                    "explanation": {"type": "string"},
                },
                "required": [
                    "question",
                    "options",
                    "correct_answer",
                    "explanation",
                ],
            },
        }
    },
    "required": ["questions"],
}


def clean_json_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
        if text.lower().startswith("json"):
            text = text[4:].lstrip()
    return text


def generate_quiz(passage: str) -> dict:
    prompt = f"""
Create exactly 3 multiple-choice questions from the educational passage below.

Passage:
{passage}

Rules:
- Each question must have exactly 4 options.
- correct_answer must be the zero-based option index: 0, 1, 2, or 3.
- Questions must test the supplied passage, not unrelated facts.
- Give a short explanation for the correct answer.
"""
    raw = clean_json_block(generate_json(prompt, QUIZ_SCHEMA))
    data = json.loads(raw)
    validated = QuizResponse.model_validate(data)
    return validated.model_dump()
