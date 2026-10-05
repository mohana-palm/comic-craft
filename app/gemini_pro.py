import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_story(outline):

    prompt = f"""
Create a comic story from this 5-panel outline.

{outline}

For every panel create:

- narration
- caption
- dialogue

Return ONLY valid JSON.

Format:

[
    {{
        "panel_number": 1,
        "narration": "Narration",
        "caption": "Caption",
        "dialogue": "Dialogue"
    }}
]
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()