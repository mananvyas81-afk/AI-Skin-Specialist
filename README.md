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
2. Upload this repository's code (do not upload `.env`).
3. Add these Space Secrets: `GROQ_API_KEY`, `DEEPGRAM_API_KEY`, and optionally `GROQ_MODEL`, `WHISPER_MODEL`, `DEEPGRAM_TTS_MODEL`.
4. Set the Space's entry point to `main.py` and add a `requirements.txt` if prompted.

Hugging Face gives you a public HTTPS address you can use from anywhere.

### Render

Create a new Web Service from GitHub, add the same variables as secret environment variables, use `pip install -e .` as the build command, and `python main.py` as the start command. Change launch settings to bind to `0.0.0.0` and a platform-provided port before deploying.

Never commit `.env` or API keys.
