from Patients_Voice import transcribe_patient_voice
from Doctors_Brain import brain_of_the_doctor
from Doctors_Voice import convert_text_to_doctor_audio
import gradio as gr

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; }

.gradio-container {
  max-width: 80rem !important;
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
  background: #f8fafc !important;
  margin: 0 auto !important;
}
.gradio-container footer { display: none !important; }
.gradio-container .prose { display: none !important; }
.gradio-container header { display: none !important; }

/* App Header */
.app-header {
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  padding: 0.875rem 2rem;
  margin-bottom: 1.5rem;
}
.header-inner {
  max-width: 80rem;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.header-left { display: flex; align-items: center; gap: 0.875rem; }
.header-logo {
  width: 2.5rem; height: 2.5rem; border-radius: 0.75rem;
  background: linear-gradient(135deg, #14b8a6, #0f766e);
  display: flex; align-items: center; justify-content: center;
  color: #fff; box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.1);
  flex-shrink: 0;
}
.header-title { font-size: 1.125rem; font-weight: 700; color: #0f172a; letter-spacing: -0.02em; line-height: 1.2; }
.header-subtitle { font-size: 0.75rem; color: #64748b; margin-top: 1px; }
.header-right { display: flex; align-items: center; gap: 0.5rem; }
.badge-clinical {
  display: inline-flex; align-items: center; gap: 0.375rem;
  padding: 0.125rem 0.625rem; border-radius: 9999px;
  font-size: 0.6875rem; font-weight: 600; background: #f0fdfa;
  color: #0f766e; border: 1px solid rgba(20, 184, 166, 0.2);
}
.badge-clinical .dot { width: 6px; height: 6px; border-radius: 50%; background: #14b8a6; }
.badge-security {
  display: inline-flex; align-items: center; gap: 0.375rem;
  padding: 0.25rem 0.625rem; border-radius: 0.5rem;
  font-size: 0.75rem; font-weight: 500; background: #f8fafc;
  color: #475569; border: 1px solid #e2e8f0;
}

/* Section Headers */
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
.section-header-left { display: flex; align-items: center; gap: 0.625rem; }
.section-icon {
  width: 1.75rem; height: 1.75rem; border-radius: 0.5rem;
  background: #f0fdfa; border: 1px solid #ccfbf1;
  display: flex; align-items: center; justify-content: center; color: #0f766e;
}
.section-title { font-size: 0.9375rem; font-weight: 700; color: #0f172a; letter-spacing: -0.015em; }
.section-step { font-size: 0.75rem; color: #64748b; font-weight: 500; }
.section-status { font-size: 0.75rem; color: #94a3b8; }

/* Clinical Cards (applied to gr.Group) */
.clinical-card {
  background: #fff !important;
  border: 1px solid rgba(226, 232, 240, 0.9) !important;
  border-radius: 1rem !important;
  padding: 1.25rem !important;
  margin-bottom: 1.25rem !important;
  box-shadow: 0 1px 2px 0 rgba(15, 23, 42, 0.02) !important;
}
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.card-label { font-size: 0.8125rem; font-weight: 600; color: #1e293b; }
.card-badge {
  display: inline-flex; align-items: center; gap: 0.25rem;
  font-size: 0.6875rem; font-weight: 500; padding: 0.125rem 0.5rem;
  border-radius: 9999px; background: rgba(240, 253, 250, 0.8);
  color: #0f766e; border: 1px solid rgba(204, 251, 241, 0.7);
}
.card-badge .dot { width: 5px; height: 5px; border-radius: 50%; background: #14b8a6; }

/* Decorative Media Tiles */
.media-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem; }
.media-tile {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 0.75rem;
  padding: 1rem; display: flex; flex-direction: column; gap: 0.75rem;
}
.media-tile-icon {
  width: 2.5rem; height: 2.5rem; border-radius: 0.5rem;
  display: flex; align-items: center; justify-content: center;
  border: 1px solid rgba(204, 251, 241, 0.8);
  background: #f0fdfa; color: #0f766e;
}
.media-tile-icon.slate { background: #f1f5f9; color: #475569; border-color: rgba(226, 232, 240, 0.6); }
.media-tile h3 { font-size: 0.8125rem; font-weight: 700; color: #0f172a; }
.media-tile p { font-size: 0.6875rem; color: #94a3b8; line-height: 1.4; }
.media-tile-top { display: flex; align-items: flex-start; justify-content: space-between; }
.tile-badge {
  font-size: 0.625rem; text-transform: uppercase; letter-spacing: 0.05em;
  font-weight: 600; padding: 0.125rem 0.5rem; border-radius: 9999px;
}
.tile-badge.required { background: #f0fdfa; color: #0f766e; border: 1px solid rgba(20, 184, 166, 0.2); }
.tile-badge.optional { background: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0; }

/* Upload Grid (actual Gradio Image/Video components) */
.upload-grid { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 1rem !important; margin-bottom: 1.25rem !important; }
.upload-grid .gr-box, .upload-grid .image-container, .upload-grid .video-wrap {
  border-radius: 0.75rem !important;
}
@media (max-width: 640px) {
  .upload-grid { grid-template-columns: 1fr !important; }
}

/* Submit Button */
.submit-btn {
  width: 100% !important;
  padding: 0.875rem 1.25rem !important;
  background: linear-gradient(135deg, #0f766e, #0d9488, #14b8a6) !important;
  color: #fff !important;
  font-weight: 600 !important;
  font-size: 0.9375rem !important;
  border: none !important;
  border-radius: 0.75rem !important;
  cursor: pointer;
  box-shadow: 0 2px 8px 0 rgba(15, 118, 110, 0.2) !important;
  margin-bottom: 1.25rem !important;
}

/* Guidance Banner */
.guidance-banner {
  background: rgba(240, 253, 250, 0.8); border: 1px solid #ccfbf1;
  border-radius: 0.75rem; padding: 0.875rem;
  display: flex; align-items: flex-start; gap: 0.75rem;
}
.guidance-icon {
  width: 2rem; height: 2rem; border-radius: 0.375rem; flex-shrink: 0;
  background: #fff; border: 1px solid rgba(20, 184, 166, 0.2);
  display: flex; align-items: center; justify-content: center;
  color: #0f766e; margin-top: 1px;
}
.guidance-text { font-size: 0.75rem; line-height: 1.6; color: #134e4a; }
.guidance-text strong { font-weight: 600; }

/* Response Panel */
.response-panel {
  min-height: 460px;
}
.response-header {
  padding: 1rem 1.5rem; border-bottom: 1px solid #f1f5f9;
  display: flex; align-items: center; justify-content: space-between;
}
.response-header-left { display: flex; align-items: center; gap: 0.5rem; font-size: 0.75rem; font-weight: 500; color: #475569; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #94a3b8; display: inline-block; }
.status-dot.active { background: #14b8a6; }
.response-model { font-size: 0.6875rem; font-family: 'Courier New', monospace; color: #94a3b8; }

.response-body {
  padding: 3rem 2rem; text-align: center;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.response-empty-icon {
  width: 5rem; height: 5rem; border-radius: 1rem;
  background: linear-gradient(135deg, #f0fdfa, rgba(204, 251, 241, 0.7));
  border: 1px solid rgba(20, 184, 166, 0.2);
  display: flex; align-items: center; justify-content: center;
  color: #0f766e; margin-bottom: 1.25rem; position: relative;
}
.response-empty-icon .plus-badge {
  position: absolute; bottom: -4px; right: -4px;
  width: 1.5rem; height: 1.5rem; border-radius: 50%; background: #fff;
  border: 1px solid #ccfbf1; display: flex; align-items: center;
  justify-content: center; color: #14b8a6; font-size: 0.75rem;
}
.response-empty-title { font-size: 1.0625rem; font-weight: 700; color: #0f172a; letter-spacing: -0.01em; }
.response-empty-desc { font-size: 0.8125rem; color: #94a3b8; margin-top: 0.5rem; line-height: 1.6; max-width: 24rem; }

.checklist { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5rem; margin-top: 1rem; }
.checklist-item {
  display: inline-flex; align-items: center; gap: 0.25rem;
  font-size: 0.6875rem; font-weight: 500; color: #475569;
  padding: 0.25rem 0.625rem; border-radius: 0.375rem;
  background: #f8fafc; border: 1px solid #e2e8f0;
}
.checklist-item svg { color: #14b8a6; flex-shrink: 0; }

.response-security { padding: 1rem 1.5rem; border-top: 1px solid #f1f5f9; display: flex; justify-content: center; }
.security-badge {
  display: inline-flex; align-items: center; gap: 0.375rem;
  padding: 0.25rem 0.75rem; border-radius: 9999px;
  background: #f8fafc; border: 1px solid rgba(226, 232, 240, 0.8);
  font-size: 0.75rem; font-weight: 500; color: #475569;
}
.security-badge svg { color: #0f766e; flex-shrink: 0; }

/* Results Body */
.results-body .gr-box {
  border-radius: 0.75rem !important;
  margin-bottom: 0.9rem !important;
}
.results-body audio { width: 100% !important; }

/* App Footer */
.app-footer { border-top: 1px solid #e2e8f0; padding: 1rem 2rem; margin-top: 1rem; }
.footer-inner {
  max-width: 80rem; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 0.75rem; color: #94a3b8;
}
.footer-brand { display: flex; align-items: center; gap: 0.5rem; }
.footer-brand .dot { width: 6px; height: 6px; border-radius: 50%; background: #0d9488; }
.footer-brand strong { font-weight: 600; color: #475569; }
.footer-links { display: flex; gap: 1.25rem; }
.footer-links a { color: #94a3b8; text-decoration: none; }
.footer-links a:hover { color: #0f766e; }

/* Responsive */
@media (max-width: 640px) {
  .app-header { padding: 0.75rem 1rem; }
  .header-right { display: none; }
  .media-grid { grid-template-columns: 1fr; }
  .footer-inner { flex-direction: column; gap: 0.5rem; text-align: center; }
}
"""


def process_inputs(audio_filepath, image_filepath, video_filepath):
    if not audio_filepath:
        raise gr.Error("Please record or upload your voice description first.")

    if not image_filepath and not video_filepath:
        raise gr.Error("Please upload a skin image or video before analysis.")

    patient_text = transcribe_patient_voice(audio_filepath)
    doctor_text = brain_of_the_doctor(
        patient_text=patient_text,
        image_filepath=image_filepath,
        video_filepath=video_filepath,
    )
    doctor_audio = convert_text_to_doctor_audio(doctor_text)

    return patient_text, doctor_text, str(doctor_audio)


def build_ui():
    demo = gr.Blocks(
        title="AI Skin Specialist - Consultation Assistant",
    )
    with demo:
        # ---- HEADER ----
        gr.HTML("""
        <div class="app-header">
          <div class="header-inner">
            <div class="header-left">
              <div class="header-logo">
                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
                </svg>
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                  <div class="header-title">AI Skin Specialist</div>
                  <span class="badge-clinical">
                    <span class="dot"></span>
                    Clinical AI v2.4
                  </span>
                </div>
                <div class="header-subtitle">Voice, image, and video-assisted dermatological triage</div>
              </div>
            </div>
            <div class="header-right">
              <div class="badge-security">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
                <span style="font-weight:500;color:#334155;">Privacy &amp; Security</span>
              </div>
            </div>
          </div>
        </div>
        """)

        # ---- MAIN TWO-COLUMN LAYOUT ----
        with gr.Row():
            # ============ LEFT COLUMN: Patient Input ============
            with gr.Column(scale=6):
                gr.HTML("""
                <div class="section-header">
                  <div class="section-header-left">
                    <div class="section-icon">
                      <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                      </svg>
                    </div>
                    <div class="section-title">Patient Consultation Input</div>
                  </div>
                  <div class="section-step">Step 1 of 2</div>
                </div>
                """)

                # Voice / Audio input card
                with gr.Group(elem_classes="clinical-card"):
                    gr.HTML("""
                    <div class="card-header">
                      <span class="card-label">Describe your skin concern</span>
                      <span class="card-badge"><span class="dot"></span> Voice or Text</span>
                    </div>
                    """)
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        show_label=False,
                    )

                # Decorative media tiles
                gr.HTML("""
                <div class="media-grid">
                  <div class="media-tile">
                    <div class="media-tile-top">
                      <div class="media-tile-icon">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        </svg>
                      </div>
                      <span class="tile-badge required">REQUIRED</span>
                    </div>
                    <div>
                      <h3>Skin Image</h3>
                      <p>High-res close-up of the affected area</p>
                    </div>
                  </div>
                  <div class="media-tile">
                    <div class="media-tile-top">
                      <div class="media-tile-icon slate">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                        </svg>
                      </div>
                      <span class="tile-badge optional">OPTIONAL</span>
                    </div>
                    <div>
                      <h3>Skin Video</h3>
                      <p>Short clip showing texture &amp; angles</p>
                    </div>
                  </div>
                </div>
                """)

                # Actual upload components, side by side in a native row
                with gr.Row(elem_classes="upload-grid"):
                    image_input = gr.Image(
                        type="filepath",
                        show_label=False,
                        sources=["upload"],
                        height=140,
                    )
                    video_input = gr.Video(
                        show_label=False,
                        sources=["upload"],
                        height=140,
                    )

                # Analyze button
                submit_btn = gr.Button(
                    value="✦  Analyze Skin Concern",
                    elem_classes="submit-btn",
                    size="lg",
                )

                # Guidance banner
                gr.HTML("""
                <div class="guidance-banner">
                  <div class="guidance-icon">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" x2="12" y1="16" y2="12"></line>
                      <line x1="12" x2="12.01" y1="8" y2="8"></line>
                    </svg>
                  </div>
                  <div class="guidance-text">
                    <strong>Clinical Recommendation:</strong>
                    For accurate assessment, ensure natural indirect lighting and include a short video showing the affected area from multiple angles.
                  </div>
                </div>
                """)

            # ============ RIGHT COLUMN: Doctor Response ============
            with gr.Column(scale=6):
                gr.HTML("""
                <div class="section-header">
                  <div class="section-header-left">
                    <div class="section-icon">
                      <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                      </svg>
                    </div>
                    <div class="section-title">Clinical Analysis &amp; Guidance</div>
                  </div>
                  <div class="section-status">Awaiting input</div>
                </div>
                """)

                # Response panel
                with gr.Group(elem_classes="clinical-card response-panel"):
                    gr.HTML("""
                    <div class="response-header">
                      <div class="response-header-left">
                        <span class="status-dot"></span>
                        <span>Differential Triage Engine</span>
                      </div>
                      <div class="response-model">Model v2.4-MED</div>
                    </div>
                    """)

                    # Empty state
                    with gr.Column(visible=True) as empty_state:
                        gr.HTML("""
                        <div class="response-body">
                          <div class="response-empty-icon">
                            <svg width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
                            </svg>
                            <div class="plus-badge">
                              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                              </svg>
                            </div>
                          </div>
                          <div class="response-empty-title">Ready for Consultation</div>
                          <div class="response-empty-desc">Your triage report, dermatological observation notes, and AI-assisted clinical guidance will generate once details are submitted.</div>
                          <div class="checklist">
                            <span class="checklist-item">
                              <svg width="12" height="12" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
                              Symptom Extraction
                            </span>
                            <span class="checklist-item">
                              <svg width="12" height="12" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
                              Lesion Feature Detection
                            </span>
                            <span class="checklist-item">
                              <svg width="12" height="12" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
                              Care Recommendation
                            </span>
                          </div>
                        </div>
                        """)

                    # Results state (hidden until analysis completes)
                    with gr.Column(visible=False, elem_classes="results-body") as results_state:
                        patient_text_display = gr.Textbox(
                            label="Patient's Transcribed Concern",
                            interactive=False,
                            lines=3,
                        )
                        doctor_text_display = gr.Textbox(
                            label="Doctor's Clinical Response",
                            interactive=False,
                            lines=5,
                        )
                        doctor_audio_output = gr.Audio(
                            label="Doctor's Voice Response",
                            type="filepath",
                            interactive=False,
                        )

                    # Footer security badge
                    gr.HTML("""
                    <div class="response-security">
                      <div class="security-badge">
                        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                        </svg>
                        Privacy &amp; Security
                      </div>
                    </div>
                    """)

        # ---- FOOTER ----
        gr.HTML("""
        <div class="app-footer">
          <div class="footer-inner">
            <div class="footer-brand">
              <span class="dot"></span>
              <strong>AI Skin Specialist</strong>
              <span style="color:#cbd5e1;">•</span>
              <span>Clinical Guidance Support &amp; Medical Triage</span>
            </div>
            <nav class="footer-links">
              <a href="#">Clinical Safety</a>
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Service</a>
            </nav>
          </div>
        </div>
        """)

        # ---- WIRE UP LOGIC ----
        def on_analyze(audio, image, video):
            if not audio:
                raise gr.Error("Please record or upload your voice description first.")
            if not image and not video:
                raise gr.Error("Please upload a skin image or video before analysis.")

            try:
                patient_text = transcribe_patient_voice(audio)
                doctor_text = brain_of_the_doctor(
                    patient_text=patient_text,
                    image_filepath=image,
                    video_filepath=video,
                )
                doctor_audio = convert_text_to_doctor_audio(doctor_text)
            except Exception as exc:
                raise gr.Error(f"Analysis failed: {exc}")

            return (
                gr.update(visible=False),   # empty_state → hide
                gr.update(visible=True),    # results_state → show
                patient_text,               # patient_text_display
                doctor_text,                # doctor_text_display
                str(doctor_audio),          # doctor_audio_output
            )

        submit_btn.click(
            fn=on_analyze,
            inputs=[audio_input, image_input, video_input],
            outputs=[empty_state, results_state, patient_text_display, doctor_text_display, doctor_audio_output],
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(
        debug=True,
        theme=gr.themes.Soft(
            primary_hue="teal",
            neutral_hue="slate",
            font=["Inter", "system-ui", "sans-serif"],
        ),
        css=CUSTOM_CSS,
    )