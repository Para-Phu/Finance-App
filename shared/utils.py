"""
shared/utils.py
───────────────
Helper functions available to every app in the portfolio.
Import with: from shared.utils import page_header, ...
"""

import streamlit as st


def page_header(title: str, description: str = "", icon: str = ""):
    """
    Renders a consistent header at the top of every app page.
    Call this as the first line inside every render() function.

    Usage:
        page_header("Budget Tool", "Upload a CSV to analyse spend.", icon="💰")
    """
    col1, col2 = st.columns([0.08, 0.92]) if icon else st.columns([1])
    if icon:
        with col1:
            st.markdown(f"<span style='font-size:2rem'>{icon}</span>", unsafe_allow_html=True)
        with col2:
            st.title(title)
            if description:
                st.caption(description)
    else:
        st.title(title)
        if description:
            st.caption(description)
    st.markdown("---")


def back_button(label: str = "← Back to Home"):
    """
    Renders a back button that returns the user to the home page.
    Useful at the bottom of long pages.
    """
    if st.button(label):
        st.session_state.current_page = "_home"
        st.rerun()


def not_yet_built(feature: str = "This feature"):
    """
    Placeholder for unfinished sections within an app.
    Keeps the page visible without throwing errors.
    """
    st.info(f"🚧 {feature} is coming soon.", icon="🔧")


def require_file_upload(label: str = "Upload a file to get started", file_types: list = None):
    """
    Standardised file uploader with a consistent prompt style.
    Returns the uploaded file object, or None.

    Usage:
        f = require_file_upload("Upload your CSV", file_types=["csv"])
        if f is None:
            return
    """
    file_types = file_types or ["csv", "xlsx"]
    uploaded = st.file_uploader(label, type=file_types)
    if uploaded is None:
        st.stop()  # Halts render() until a file is uploaded
    return uploaded


def section(title: str):
    """Renders a consistent section sub-heading."""
    st.markdown(f"### {title}")
