import gradio as gr
from app.styles import APP_CSS
from app.ui import build_ui


if __name__ == "__main__":
    app = build_ui()
    app.launch(
        debug=False,
        theme=gr.themes.Soft(
            primary_hue="green",
            neutral_hue="slate",
            font=["DM Sans", "system-ui", "sans-serif"],
        ),
        css=APP_CSS,
    )
