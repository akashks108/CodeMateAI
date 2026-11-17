import os
from google import genai
from django.conf import settings


# Generate a programming lesson based on the selected curriculum topic
def generate_lesson(language, level, topic, description=""):

    api_key = settings.GEMINI_API_KEY

    if not api_key:
        raise ValueError("Gemini API key is not configured.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are CodeMate AI, a friendly programming teacher.

    Teach this curriculum topic:
    Language: {language}
    Level: {level}
    Topic: {topic}
    Description: {description}

    Follow this exact lesson structure:

    ## 1. What is it?
    Explain the concept in 2-3 simple sentences.

    ## 2. How does it work?
    Explain the main idea in simple steps.

    ## 3. Syntax
    Show the basic syntax with a short code example.

    ## 4. Example
    Give one practical code example and briefly explain it.

    ## 5. Remember
    Give 2-3 important points.

    ## 6. Practice
    Give one small exercise for the student.

    RULES:
    - Keep the entire lesson under 250 words.
    - Use simple language suitable for the selected level.
    - Avoid unnecessary introductions and conclusions.
    - Do not repeat explanations.
    - Use short paragraphs and bullet points.
    - Keep code examples short and relevant.
    - Teach only the selected topic.
    - Do not include the answers to the practice exercise.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "max_output_tokens": 700,
            "temperature": 0.4
        }
    )

    return response.text

# Generate a new practice question for the selected topic
def generate_practice_question(language, level, topic, description=""):

    api_key = settings.GEMINI_API_KEY

    if not api_key:
        raise ValueError("Gemini API key is not configured.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are CodeMate AI, a programming practice teacher.

    Generate ONE new programming exercise.

    Programming Language: {language}
    Learning Level: {level}
    Topic: {topic}
    Topic Description: {description}

    RULES:
    - Generate exactly one practical programming question.
    - The question must test the selected topic.
    - Match the difficulty to the student's learning level.
    - Use simple and clear instructions.
    - Do not provide the solution or code answer.
    - Do not repeat a basic example from the lesson.
    - Return only the question, without an introduction.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "max_output_tokens": 200,
            "temperature": 0.7
        }
    )

    return response.text