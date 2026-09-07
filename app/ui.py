import gradio as gr
from app.services import analyze_consultation


def build_ui():
    with gr.Blocks(title="AI Skin Specialist", fill_width=True) as demo:
        gr.HTML("""
          <section class="hero">
            <p class="kicker">AI Skin Specialist</p>
            <h1>Clearer skin guidance, <em>thoughtfully tailored.</em></h1>
            <p>Share what you are experiencing and a clear photo. We will turn your inputs into cautious, practical skin-care guidance and an optional spoken summary.</p>
          </section>
        """)
        with gr.Row(equal_height=True):
            with gr.Column(scale=1, min_width=320):
                gr.HTML('<p class="step-label">Step 1 — Your consultation</p><h2 class="section-title">Tell us what is happening</h2>')
                with gr.Group(elem_classes="card"):
                    gr.HTML('<div class="label-wrap"><span>Required</span><h3>Voice description</h3></div>')
                    audio = gr.Audio(sources=["microphone", "upload"], type="filepath", show_label=False)
                    gr.HTML('<div class="label-wrap"><span>Required</span><h3>Clear skin image</h3></div>')
                    image = gr.Image(sources=["upload", "webcam"], type="filepath", show_label=False, height=220)
                    gr.HTML('<div class="label-wrap"><span>Optional</span><h3>Short video</h3></div>')
                    video = gr.Video(sources=["upload"], show_label=False, height=160)
                    analyze = gr.Button("Create my skin guidance  →", variant="primary")
                    gr.HTML('<div class="disclaimer"><strong>For guidance, not diagnosis.</strong> This tool cannot replace a qualified dermatologist. Seek urgent care for rapidly spreading rashes, severe pain, swelling, breathing difficulty, or signs of infection.</div>')

            with gr.Column(scale=1, min_width=320):
                gr.HTML('<p class="step-label">Step 2 — Your results</p><h2 class="section-title">A considered next step</h2>')
                with gr.Group(elem_classes="card"):
                    with gr.Column(visible=True) as empty:
                        gr.HTML('<div class="empty-state"><div class="icon">✦</div><h2>Ready when you are</h2><p>Your transcript, practical guidance, and voice response will appear here after you submit your consultation.</p></div>')
                    with gr.Column(visible=False) as results:
                        gr.HTML('<h2 class="result-heading">Your skin guidance</h2>')
                        transcript = gr.Textbox(label="What we heard", interactive=False, lines=3)
                        guidance = gr.Textbox(label="AI-assisted guidance", interactive=False, lines=7)
                        spoken = gr.Audio(label="Spoken response", type="filepath", interactive=False)

        gr.HTML('<p class="footer-note">AI Skin Specialist • Privacy-conscious, general skin-care guidance</p>')

        def submit(audio_path, image_path, video_path):
            try:
                transcript_text, guidance_text, audio_response = analyze_consultation(audio_path, image_path, video_path)
            except ValueError as error:
                raise gr.Error(str(error))
            except Exception:
                raise gr.Error("We could not complete the analysis. Please check your connection and try again.")
            return gr.update(visible=False), gr.update(visible=True), transcript_text, guidance_text, audio_response

        analyze.click(submit, [audio, image, video], [empty, results, transcript, guidance, spoken])
    return demo
