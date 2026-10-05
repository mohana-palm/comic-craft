import os
import json
import time

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Try different Gemini text models
MODELS = [
    "gemini-flash-lite-latest",
    "gemini-flash-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash"
]


def generate_outline(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):

    prompt = f"""
Create a 5-panel comic outline.

Story:
{story_prompt}

Character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Return ONLY valid JSON.

Format:

[
    {{
        "panel_number": 1,
        "title": "Panel title",
        "scene_description": "Scene description",
        "image_prompt": "Image prompt"
    }}
]
"""

    last_error = None

    for model in MODELS:

        print()
        print("=" * 50)
        print(f"Trying Gemini model: {model}")
        print("=" * 50)

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                text = response.text.strip()

                # Remove JSON code fences
                if text.startswith("```json"):
                    text = text[7:]

                if text.startswith("```"):
                    text = text[3:]

                if text.endswith("```"):
                    text = text[:-3]

                result = json.loads(text.strip())

                print()
                print(f"SUCCESS: {model}")
                print()

                return result

            except Exception as e:

                last_error = e

                print(
                    f"Model {model} failed "
                    f"(attempt {attempt + 1}):"
                )

                print(e)

                if attempt == 0:
                    print("Waiting 3 seconds...")
                    time.sleep(3)

        print()
        print(f"Moving to next model...")
        print()

    raise RuntimeError(
        "All Gemini text models failed. "
        f"Last error: {last_error}"
    )