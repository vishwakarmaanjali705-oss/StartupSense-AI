"""
style.py - makes the Streamlit app match the StartupSense AI homepage.

Usage in app.py (right after st.set_page_config):

    from style import apply_style, hero, card
    apply_style()
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

:root{
  --bg:#fffaf5; --bg-soft:#fdf0e8; --text:#3b2f2f; --muted:#7d6b68;
  --primary:#e8743b; --pink:#f2a0b5; --border:rgba(120,80,60,.15);
}

/* ---------- Base ---------- */
html, body, [class*="css"], .stApp { font-family:'Inter', sans-serif; color:var(--text); }
.stApp {
  background:
    radial-gradient(600px 400px at 8% 0%, rgba(242,160,181,.28), transparent 60%),
    radial-gradient(600px 400px at 95% 5%, rgba(246,184,138,.28), transparent 60%),
    var(--bg);
}
h1, h2, h3, h4 { font-family:'Space Grotesk','Inter',sans-serif !important; color:var(--text); }
.block-container { padding-top:2.5rem; max-width:1100px; }

/* Hide default Streamlit menu + footer */
#MainMenu, footer { visibility:hidden; }
header[data-testid="stHeader"] { background:transparent; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
  background:var(--bg-soft);
  border-right:1px solid var(--border);
}

/* ---------- Buttons ---------- */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
  background:linear-gradient(135deg,#e8743b,#ee8fa6);
  color:#fff; border:0; border-radius:999px;
  padding:.65rem 1.6rem; font-weight:600;
  box-shadow:0 8px 22px rgba(232,116,59,.30);
  transition:all .25s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  transform:translateY(-2px);
  box-shadow:0 12px 28px rgba(232,116,59,.42);
  color:#fff; border:0;
}

/* ---------- Inputs ---------- */
.stTextInput input, .stTextArea textarea, .stNumberInput input,
div[data-baseweb="select"] > div {
  background:#fff !important; border:1px solid var(--border) !important;
  border-radius:12px !important; color:var(--text) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
  border-color:var(--primary) !important;
  box-shadow:0 0 0 3px rgba(232,116,59,.15) !important;
}
label, .stMarkdown p { color:var(--text); }

/* ---------- Forms, tabs, expanders, metrics ---------- */
[data-testid="stForm"] {
  background:#fff; border:1px solid var(--border); border-radius:18px;
  padding:1.6rem; box-shadow:0 14px 36px rgba(190,120,90,.12);
}
.stTabs [data-baseweb="tab-list"] { gap:6px; }
.stTabs [data-baseweb="tab"] {
  background:#fff; border-radius:999px; padding:8px 20px; border:1px solid var(--border);
}
.stTabs [aria-selected="true"] { background:var(--primary); color:#fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display:none; }
[data-testid="stExpander"] {
  background:#fff; border:1px solid var(--border); border-radius:14px;
}
[data-testid="stMetric"] {
  background:#fff; border:1px solid var(--border); border-radius:16px; padding:16px;
}

/* ---------- Custom components ---------- */
.ss-hero {
  text-align:center; padding:2.2rem 1rem 1.6rem;
}
.ss-hero h1 {
  font-size:2.6rem; margin-bottom:.4rem;
  background:linear-gradient(135deg,#e8743b,#e0709a);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
.ss-hero p { color:var(--muted); font-size:1.05rem; max-width:620px; margin:0 auto; }
.ss-card {
  background:#fff; border:1px solid var(--border); border-radius:18px;
  padding:1.4rem 1.6rem; margin:.6rem 0;
  box-shadow:0 6px 20px rgba(190,120,90,.10);
}
.ss-card h4 { margin:0 0 .4rem; }
.ss-card p { color:var(--muted); margin:0; }
</style>
"""


def apply_style():
    """Inject the global theme CSS. Call once near the top of app.py."""
    st.markdown(CSS, unsafe_allow_html=True)


def hero(title, subtitle=""):
    """Big gradient page title, like the homepage hero."""
    st.markdown(
        '<div class="ss-hero"><h1>' + title + '</h1><p>' + subtitle + '</p></div>',
        unsafe_allow_html=True,
    )


def card(title, body):
    """A soft white card. Good for showing the AI analysis result."""
    st.markdown(
        '<div class="ss-card"><h4>' + title + '</h4><p>' + body + '</p></div>',
        unsafe_allow_html=True,
    )