# AI Skin Specialist

An **AI-based Medical Skin Specialist** is a multimodal health-information and decision-support prototype that analyzes a user's skin image along with an optional text or voice query. It uses vision and language models to generate a **preliminary, non-diagnostic explanation** and can provide the response in both text and speech. 

## Features

* 🖼️ **Skin Image Analysis** – Analyzes uploaded images to identify visible skin features.
* 💬 **Text & Voice Queries** – Allows users to ask questions using text or voice.
* 🎙️ **Speech-to-Text** – Converts voice input into text.
* 🤖 **AI-Based Analysis** – Combines image information with the user's query to generate a response.
* 🔊 **Text-to-Speech** – Converts the generated response into audio.
* ⚕️ **Safety Guidance** – Indicates when professional medical evaluation may be appropriate.
* 🌐 **Web Interface** – Provides image upload, input, response display, and audio playback. 

## Technologies Used

* **Python**
* **Gradio**
* **Multimodal LLM / Vision Model**
* **Speech-to-Text (STT)**
* **Text-to-Speech (TTS)**
* **Groq / Compatible AI API**
* **ElevenLabs / Deepgram** 

## Project Objectives

The project aims to make basic skin-related health information more accessible by allowing users to upload a skin image, ask questions through text or voice, and receive clear AI-generated guidance. 

## Disclaimer

This project is a **health-information and decision-support prototype**. It does not provide a confirmed medical diagnosis, replace a dermatologist, prescribe medication, or guarantee accuracy. Users should seek professional medical advice when necessary. 

## Future Scope

Future improvements may include a clinically reviewed knowledge base, structured symptom questions, image-quality checks, clinician referral workflows, multilingual voice interaction, and evaluation using properly sourced datasets. 

## Pipeline

Image input -> Preprocessing (orientation fix, resize, contrast, quality check) -> Vision model (Llama-4 via Groq) -> Skin condition prediction -> Top-3 predictions with confidence.

## Evaluation

`python eval.py` runs the model on labelled images in `test_data/<condition>/` and reports accuracy, precision, recall, F1 and a confusion matrix (saved to `metrics.txt`).

## Lightweight / Mobile Access

The system uses a lightweight vision model through a cloud API, so it works from a phone browser with no on-device compute. Future work: fine-tune MobileNetV2 via transfer learning on a dermatology dataset (e.g., HAM10000) for offline use.

## Limitations and Research Gaps

Skin-tone bias, need for more diverse datasets, and lack of external clinical validation. Confidence values are the model's own estimates, not calibrated probabilities.
