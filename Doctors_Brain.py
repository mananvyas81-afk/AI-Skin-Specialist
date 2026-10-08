import base64
import json
import os
import re
from io import BytesIO

from dotenv import load_dotenv
from groq import Groq
from PIL import Image, ImageOps, ImageStat


load_dotenv()


def preprocess_image(filepath):
    """Pipeline step 2: preprocessing. Returns (clean PIL image, quality notes)."""
    image = ImageOps.exif_transpose(Image.open(filepath)).convert("RGB")
    notes = []
    if min(image.size) < 200:
        notes.append("Low resolution - use a closer, higher-quality photo.")
    brightness = ImageStat.Stat(image.convert("L")).mean[0]
    if brightness < 60:
        notes.append("Image is dark - retake in better light.")
    elif brightness > 200:
        notes.append("Image is overexposed - avoid direct flash.")
    image.thumbnail((1024, 1024))            # resize
    image = ImageOps.autocontrast(image, 1)  # normalise contrast
    return image, (notes or ["Image quality is acceptable."])


def encode_image_for_groq(image):
    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=75)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def parse_prediction(text):
    """Parse the model's JSON output; fall back to plain text if it is not valid."""
    try:
        data = json.loads(re.sub(r"^```(?:json)?|```$", "", text.strip()).strip())
        preds = [
            (str(p["condition"]), float(p["confidence"]))
            for p in data.get("predictions", [])
        ][:3]
        preds.sort(key=lambda x: x[1], reverse=True)
        return preds, str(data.get("guidance", "")).strip() or text
    except Exception:
        return [], text


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
    clean_image, quality_notes = preprocess_image(image_filepath)
    image_data = encode_image_for_groq(clean_image)

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
        "Reply ONLY with JSON: {\"predictions\": [{\"condition\": str, \"confidence\": number 0-100}, "
        "...up to 3 most likely visible skin conditions], "
        "\"guidance\": \"2 or 3 plain sentences: visible concerns, possible general causes, safe next steps\"}. "
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
                "qwen/qwen3.8-27b"
            ),
            max_completion_tokens=2000,
            response_format={"type": "json_object"},
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
    raw = response.choices[0].message.content.strip()
    predictions, guidance = parse_prediction(raw)

    return {
        "guidance": guidance,
        "predictions": predictions,       # [(condition, confidence %), ...]
        "quality_notes": quality_notes,
        "preprocessed_image": clean_image,
    }
