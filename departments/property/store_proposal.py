"""
departments/property/store_proposal.py

Loaded dynamically by app.py via importlib — must expose a render() function.
Do NOT call st.set_page_config() here; app.py already calls it.

Share link flow:
  1. User clicks "Copy shareable link" in the HTML tool.
  2. HTML builds: https://<root>/?current_page=store_proposal&<all inputs as params>
  3. Recipient opens the link → app.py sees current_page=store_proposal, sets session
     state, and calls this render() function.
  4. render() reads the remaining query params and injects them as
     window.STREAMLIT_PARAMS so the HTML pre-fills all inputs.
"""

import streamlit as st
import json
from pathlib import Path


def render():
    # ── Load the HTML file ────────────────────────────────────────────────────
    HTML_PATH = Path(__file__).parent.parent.parent / "new-store-proposal-app-live.html"
    html_source = HTML_PATH.read_text(encoding="utf-8")

    # ── Detect base URL for share links ──────────────────────────────────────
    # The app is a single-page router so base URL is always the root domain.
    try:
        headers  = dict(st.context.headers)
        host     = headers.get("host", "").split(",")[0].strip()
        is_https = "streamlit.app" in host or headers.get("x-forwarded-proto", "") == "https"
        base_url = f"{'https' if is_https else 'http'}://{host}" if host else "https://finance-app-para-commercial.streamlit.app"
    except Exception:
        base_url = "https://finance-app-para-commercial.streamlit.app"

    # ── Read HTML tool params from the URL (skip the routing param) ───────────
    raw_params = {k: v for k, v in st.query_params.items() if k != "current_page"}

    # ── Build JS injection ────────────────────────────────────────────────────
    # window.STREAMLIT_BASE   → root URL so share links are built correctly
    # window.STREAMLIT_PARAMS → pre-fill inputs when opening a share link
    inject_lines = [f"window.STREAMLIT_BASE = {json.dumps(base_url)};"]
    if raw_params:
        inject_lines.append(f"window.STREAMLIT_PARAMS = {json.dumps(raw_params)};")

    inject_script = "<script>" + "\n".join(inject_lines) + "</script>"
    html_source   = html_source.replace("</head>", inject_script + "\n</head>", 1)

    # ── Render ────────────────────────────────────────────────────────────────
    st.components.v1.html(html_source, height=2800, scrolling=True)
