---
title: AI Skin Specialist
emoji: ✨
colorFrom: green
colorTo: pink
sdk: gradio
app_file: main.py
pinned: false
---

# AI Skin Specialist

A Gradio application that combines a patient voice description, a skin image, and optional video into cautious AI-assisted skin-care guidance.

> **Clinical safety:** This app provides general information only. It is not a diagnostic tool or a replacement for a licensed clinician.

## Project structure

```text
.
├── app/
│   ├── services.py       # Orchestrates transcription, analysis, and voice output
│   ├── styles.py         # Central visual design system (CSS)
│   └── ui.py             # Gradio interface and event wiring
├── main.py               # Small application entry point
├── Doctors_Brain.py      # Groq vision-language guidance
├── Doctors_Voice.py      # Deepgram text-to-speech
├── Patients_Voice.py     # Groq speech-to-text
├── pyproject.toml        # Python dependencies
├── requirements.txt      # Deployment-friendly dependency list
└── .env.example          # Required environment variable names
```

## Run locally

1. Install Python 3.11 or newer.
2. Install dependencies: `pip install -e .`
3. Copy `.env.example` to `.env`, then add your API keys.
4. Run: `python main.py`

## Deployment

Deploy this as a Python web app—not GitHub Pages—because it needs server-side API keys.

### Hugging Face Spaces (recommended)

1. Create a new **Gradio** Space.
2. Select **Files → Add file → Upload files** and upload this project, or connect the repository.
3. In **Settings → Repository secrets**, add `GROQ_API_KEY` and `DEEPGRAM_API_KEY`. Optional overrides are listed in `.env.example`.
4. The Space automatically starts `main.py` from the metadata at the top of this README.

Hugging Face gives you a public HTTPS URL usable from any device.

### Render

Create a Web Service from this GitHub repository and set:

- Build command: `pip install -r requirements.txt`
- Start command: `python main.py`
- Secret environment variables: `GROQ_API_KEY` and `DEEPGRAM_API_KEY`

The app reads Render's `PORT` automatically.

Never commit `.env` or API keys.
