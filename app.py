import streamlit as st

with open("new-store-proposal-app-live.html", "r") as f:
    html_content = f.read()

st.set_page_config(page_title="Finance App", layout="wide")
st.components.v1.html(html_content, height=900, scrolling=True)
