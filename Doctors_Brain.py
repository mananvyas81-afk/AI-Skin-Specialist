import base64
import os
from io import BytesIO

from dotenv import load_dotenv
from groq import Groq
from PIL import Image


load_dotenv()


def encode_image_for_groq(filepath):
    image = Image.open(filepath)
    image.thumbnail((1024, 1024))

    buffer = BytesIO()
    image.convert("RGB").save(
        buffer,
        format="JPEG",
        quality=75
    )

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def brain_of_the_doctor(patient_text, image_filepath=None, video_filepath=None):

    groq_api_key = os.environ.get("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY in .env or environment")

    if not image_filepath:
        raise ValueError(
            "Please upload a skin image. The current Groq vision model requires an image."
        )

    # -----------------------------------------
    # Encode image
    # -----------------------------------------
    image_data = encode_image_for_groq(image_filepath)

    # -----------------------------------------
    # Keep patient text safely below API limit
    # -----------------------------------------
    patient_text = str(patient_text or "").strip()

    # Reserve room for instructions and labels.
    MAX_PATIENT_TEXT = 1000

    if len(patient_text) > MAX_PATIENT_TEXT:
        patient_text = patient_text[:MAX_PATIENT_TEXT].rsplit(" ", 1)[0]
        patient_text += "..."

    # -----------------------------------------
    # Short prompt
    # -----------------------------------------
    prompt = (
        "Analyze the uploaded skin image as a careful skin care assistant. "
        "Give general information, not a diagnosis. "
        "Mention visible skin concerns, possible general causes, and basic safe next steps. "
        "Do not claim certainty. "
        "Answer in 2 or 3 short sentences. "
        "Use plain text only, with no markdown or symbols. "
        f"Patient description: {patient_text}"
    )

    if video_filepath:
        prompt += (
            " The patient also uploaded a video. "
            "This analysis uses the uploaded image because this model does not directly analyze video."
        )

    # -----------------------------------------
    # Debug information
    # -----------------------------------------
    print("\n========== GROQ REQUEST ==========")
    print("Patient text characters:", len(patient_text))
    print("Prompt characters:", len(prompt))
    print("Image base64 characters:", len(image_data))
    print("==================================\n")

    # Safety check
    if len(prompt) > 1900:
        raise ValueError(
            f"Prompt is still too long: {len(prompt)} characters. "
            "Please shorten the patient description."
        )

    # -----------------------------------------
    # Groq request
    # -----------------------------------------
    client = Groq(api_key=groq_api_key)

    try:
        response = client.chat.completions.create(
            model=os.environ.get(
                "GROQ_MODEL",
                "meta-llama/llama-4-scout-17b-16e-instruct"
            ),
            max_completion_tokens=300,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful skin care assistant. "
                        "Give general information, not a diagnosis."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        },
                    ],
                },
            ],
        )

    except Exception as e:
        print("Groq API error:", e)
        raise ValueError(
            f"Skin analysis failed: {str(e)}"
        )

    # -----------------------------------------
    # Return doctor's response
    # -----------------------------------------
    result = response.choices[0].message.content.strip()

    return result