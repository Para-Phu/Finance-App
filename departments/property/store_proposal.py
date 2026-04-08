import streamlit as st
import streamlit.components.v1 as components
import os

def render():
    html_path = os.path.join(os.path.dirname(__file__), "../../new-store-proposal-app-live.html")
    with open(html_path, "r") as f:
        html_content = f.read()
    components.html(html_content, height=900, scrolling=True)
