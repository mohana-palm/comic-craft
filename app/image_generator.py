import os

from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    api_key=os.environ["HF_TOKEN"]
)

OUTPUT_DIR = "static/panels"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


def generate_image(
    image_prompt,
    panel_number
):

    prompt = f"""
Create a high-quality colorful comic-book illustration.

Scene:
{image_prompt}

Style:
Comic book art, colorful, detailed,
adventure atmosphere, cinematic lighting.

Do not include any text,
captions, speech bubbles,
or words inside the image.
"""

    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )

    filename = f"panel_{panel_number}.png"

    filepath = os.path.join(
        OUTPUT_DIR,
        filename
    )

    image.save(filepath)

    print(
        f"Panel {panel_number} image saved: "
        f"{filepath}"
    )

    return f"/static/panels/{filename}"