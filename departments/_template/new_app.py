"""
departments/_template/new_app.py
──────────────────────────────────
Copy this file into the correct department folder to start a new app.

Steps:
  1. Copy to e.g. departments/ops/my_new_tool.py
  2. Add an entry to the NAV dict in app.py
  3. Replace the content of render() with your app logic
"""

import streamlit as st
from shared.utils import page_header, back_button, section


def render():
    page_header(
        title="New App Title",
        description="One sentence describing what this app does.",
        icon="🔧",   # pick a relevant emoji
    )

    section("Section One")
    st.write("Add your Streamlit content here.")

    section("Section Two")
    st.write("Each section() call renders a consistent sub-heading.")

    back_button()
