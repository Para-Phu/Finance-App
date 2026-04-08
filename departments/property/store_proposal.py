import streamlit as st, json

params = dict(st.query_params)
with open("new-store-proposal-app-live.html") as f:
    html = f.read()

inject = f"<script>window.STREAMLIT_PARAMS = {json.dumps(params)};</script>"
html = html.replace("</head>", inject + "</head>")

st.components.v1.html(html, height=1800, scrolling=True)
