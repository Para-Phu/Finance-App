"""
departments/property/store_proposal.py

Loaded dynamically by app.py via importlib — must expose a render() function.
Do NOT call st.set_page_config() here; app.py already calls it.
"""

import streamlit as st
import json
from pathlib import Path

# ── Hardcoded base URL ────────────────────────────────────────────────────────
# This is the root URL of the app (single-page router — no sub-paths).
# The share link includes ?current_page=store_proposal so app.py routes correctly.
SHARE_BASE_URL = "https://finance-app-para-commercial.streamlit.app"


def render():
    # ── Scroll parent to top on every navigation to this page ────────────────
    # Fixes the "page loads scrolled to the bottom" issue caused by height=2800.
    st.components.v1.html(
        "<script>window.parent.scrollTo({ top: 0, behavior: 'instant' });</script>",
        height=0,
    )

    # ── Load the HTML file ────────────────────────────────────────────────────
    HTML_PATH = Path(__file__).parent.parent.parent / "new-store-proposal-app-live.html"
    html_source = HTML_PATH.read_text(encoding="utf-8")

    # ── Read tool input params from the URL (strip the routing param) ─────────
    raw_params = {k: v for k, v in st.query_params.items() if k != "current_page"}

    # ── Inject JS globals ─────────────────────────────────────────────────────
    # window.STREAMLIT_BASE   → root URL used when building share links
    # window.STREAMLIT_PARAMS → pre-fill form inputs when opening a share link
    inject_lines = [f"window.STREAMLIT_BASE = {json.dumps(SHARE_BASE_URL)};"]
    if raw_params:
        inject_lines.append(f"window.STREAMLIT_PARAMS = {json.dumps(raw_params)};")

    inject_script = "<script>" + "\n".join(inject_lines) + "</script>"
    html_source = html_source.replace("</head>", inject_script + "\n</head>", 1)

    # ── Render ────────────────────────────────────────────────────────────────
    st.components.v1.html(html_source, height=2800, scrolling=True)
