import streamlit as st
import streamlit.components.v1 as components
import os

def render():
    html_path = os.path.join(os.path.dirname(__file__), "../../new-store-proposal-app-live.html")
    with open(html_path, "r") as f:
        html_content = f.read()
    components.html(html_content, height=900, scrolling=True)

import streamlit as st

# Read any incoming query params
params = st.query_params.to_dict()
params_json = str(params).replace("'", '"')  # basic JSON-ish pass

# Inject params into the HTML as a JS variable before rendering
with open("new-store-proposal-app-live.html", "r") as f:
    html = f.read()

# Inject the params right before </head>
inject = f"<script>window.STREAMLIT_PARAMS = {params_json};</script>"
html = html.replace("</head>", inject + "</head>")

st.components.v1.html(html, height=1800, scrolling=True)
