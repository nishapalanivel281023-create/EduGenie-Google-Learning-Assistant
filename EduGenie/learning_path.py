from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for this topic:

{topic}

Assume the learner is a beginner unless the input explicitly says otherwise.

Include:
1. Goal
2. Beginner foundations
3. Intermediate topics
4. Advanced topics
5. A suggested weekly progression
6. Practice/project ideas
7. Reliable resource types to look for (official documentation, textbooks,
   reputable courses, tutorials, or videos)

Do not invent specific URLs. Keep the plan practical and easy to follow.
"""
    return generate_text(prompt)
