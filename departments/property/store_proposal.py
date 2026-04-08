"""
departments/property/store_proposal.py
New Store / Acquisition & Conversion – Directional Assessment

Streamlit wrapper for the self-contained HTML tool.
• Reads st.query_params and injects them as window.STREAMLIT_PARAMS
  so the HTML's loadFromURL() pre-fills all inputs from a shared link.
• Shareable links resolve to THIS page (not the app root), so the
  HTML's STREAMLIT_BASE constant must point here too.
"""

import streamlit as st
import json
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Store Proposal",
    page_icon="🏪",
    layout="centered",
)

# ── Load the HTML file ───────────────────────────────────────────────────────
HTML_PATH = Path(__file__).parent.parent.parent / "new-store-proposal-app-live.html"
html_source = HTML_PATH.read_text(encoding="utf-8")

# ── Read query params from the Streamlit URL ─────────────────────────────────
# st.query_params returns a dict-like object; convert to plain dict.
raw_params: dict = dict(st.query_params)

# ── Inject params as a JS global BEFORE the HTML body runs ───────────────────
# The HTML already checks for window.STREAMLIT_PARAMS in loadFromURL().
# We prepend a <script> block that sets that global.
if raw_params:
    inject_script = (
        "<script>"
        f"window.STREAMLIT_PARAMS = {json.dumps(raw_params)};"
        "</script>"
    )
    # Insert just before </head> so it runs before the body's inline script.
    html_source = html_source.replace("</head>", inject_script + "</head>", 1)

# ── Render ───────────────────────────────────────────────────────────────────
# height: enough to show the full tool without a double scroll bar.
# scrolling=True lets the iframe scroll internally on mobile.
st.components.v1.html(html_source, height=2800, scrolling=True)
