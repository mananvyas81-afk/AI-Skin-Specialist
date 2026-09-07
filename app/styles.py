APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root { --ink:#20372b; --muted:#637268; --cream:#f8f6ef; --sage:#dce7da; --moss:#356247; --peach:#f2c7b5; --line:#d9e1d7; }
body, .gradio-container { background:var(--cream)!important; font-family:'DM Sans',sans-serif!important; color:var(--ink)!important; }
.gradio-container { max-width:1240px!important; margin:0 auto!important; padding:0 4vw 3rem!important; }
footer, .gradio-container > .main > .wrap > .contain > .footer { display:none!important; }
.hero { margin:1.5rem 0 2.2rem; padding:clamp(2rem,5vw,4.8rem); overflow:hidden; position:relative; border-radius:28px; background:var(--sage); }
.hero:after { content:''; position:absolute; width:260px; height:260px; right:-60px; top:-100px; border-radius:50%; background:#f6d78d; opacity:.8; }
.kicker { margin:0 0 .7rem; color:var(--moss); text-transform:uppercase; letter-spacing:.14em; font-size:.72rem; font-weight:700; }
.hero h1 { max-width:680px; margin:0; font-family:'Playfair Display',serif; font-size:clamp(2.4rem,5vw,4.5rem); line-height:1.05; letter-spacing:-.04em; }
.hero h1 em { color:var(--moss); font-style:normal; }.hero p:last-child { max-width:560px; margin:1rem 0 0; color:var(--muted); font-size:1.05rem; }
.step-label { margin:0 0 .8rem; color:var(--moss); text-transform:uppercase; letter-spacing:.12em; font-size:.7rem; font-weight:700; }.section-title { margin:0 0 1.2rem; font-size:1.28rem; letter-spacing:-.02em; }
.card { background:#fff!important; border:1px solid var(--line)!important; border-radius:20px!important; padding:1.35rem!important; box-shadow:0 10px 30px rgba(35,55,43,.05)!important; }
.card .label-wrap span { color:var(--muted); font-size:.82rem; }.card .label-wrap h3 { margin:.15rem 0 1rem; font-size:1rem; }
.gr-button-primary { background:var(--moss)!important; border:0!important; border-radius:999px!important; min-height:48px!important; font-weight:700!important; }.gr-button-primary:hover { filter:brightness(.93); }
textarea, input { border-radius:12px!important; }.output .wrap { border-radius:14px!important; }.disclaimer { margin-top:1rem; padding:1rem 1.1rem; border-left:3px solid var(--peach); background:#fff7f2; color:#775e52; border-radius:0 10px 10px 0; font-size:.82rem; line-height:1.5; }
.result-heading { margin:0 0 1rem; font-family:'Playfair Display',serif; font-size:1.8rem; }.empty-state { min-height:390px; display:grid; align-content:center; text-align:center; padding:2rem; color:var(--muted); }.empty-state .icon { margin:auto auto 1rem; width:64px; height:64px; display:grid; place-items:center; border-radius:50%; background:var(--sage); color:var(--moss); font-size:1.8rem; }.empty-state h2 { color:var(--ink); font-family:'Playfair Display',serif; margin:0 0 .5rem; }.footer-note { margin:2.2rem 0 0; text-align:center; color:var(--muted); font-size:.76rem; }
@media(max-width:700px) { .gradio-container { padding:0 1rem 2rem!important; }.hero { margin-top:1rem; border-radius:20px; }.hero:after { opacity:.5; }.card { padding:1rem!important; } }
"""