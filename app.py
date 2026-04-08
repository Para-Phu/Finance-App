import streamlit as st
import importlib
import sys
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="App Portfolio",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS injection ────────────────────────────────────────────────────────────
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "shared", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ── Navigation ───────────────────────────────────────────────────────────────
NAV = {
    "Home": {
        "_home": {"label": "Overview", "module": None}
    },
    "Finance": {
        "budget_tool":    {"label": "Budget Tool",        "module": "departments.finance.budget_tool"},
        "forecast":       {"label": "Forecast",           "module": "departments.finance.forecast"},
    },
    "Operations": {
        "logistics":      {"label": "Logistics Tracker",  "module": "departments.ops.logistics"},
    },
    "Marketing": {
        "dashboard":      {"label": "Campaign Dashboard", "module": "departments.marketing.dashboard"},
    },
    "Property": {
        "store_proposal": {"label": "New Store Proposal", "module": "departments.property.store_proposal"},
    },
}

if "current_page" not in st.session_state:
    st.session_state.current_page = "_home"

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("App Portfolio")
    st.markdown("---")

    for dept_label, pages in NAV.items():
        st.markdown(f"**{dept_label}**")
        for page_key, page_info in pages.items():
            active = st.session_state.current_page == page_key
            if st.button(
                page_info["label"],
                key=f"nav_{page_key}",
                use_container_width=True,
                type="secondary" if active else "tertiary",
            ):
                st.session_state.current_page = page_key
                st.rerun()

    st.markdown("---")
    st.caption("Built with Streamlit")

# ── Router ───────────────────────────────────────────────────────────────────
current = st.session_state.current_page

if current == "_home":

    # Hero
    st.markdown("""
        <div style="
            border-top: 1px solid #1a1a1a;
            padding-top: 1.75rem;
            margin-bottom: 2.75rem;
        ">
            <p style="
                font-size: 0.58rem;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                color: #bbb;
                margin: 0 0 0.5rem;
            ">App Portfolio</p>
            <p style="
                font-size: 1.5rem;
                font-weight: 400;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                color: #1a1a1a;
                margin: 0 0 0.65rem;
                line-height: 1.15;
            ">Internal Tools</p>
            <p style="
                font-size: 0.82rem;
                color: #888;
                margin: 0;
                max-width: 400px;
                line-height: 1.75;
            ">A collection of tools for finance, operations, marketing, and property.</p>
        </div>
    """, unsafe_allow_html=True)

    # Department sections
    for dept_label, pages in NAV.items():
        if dept_label == "Home":
            continue

        items = list(pages.items())

        # Department label
        st.markdown(f"""
            <p style="
                font-size: 0.58rem;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                color: #bbb;
                margin: 0 0 0.6rem;
                border-top: 1px solid #d8d8d8;
                padding-top: 1.1rem;
            ">{dept_label}</p>
        """, unsafe_allow_html=True)

        # Cards: rendered as HTML grid so border-radius is fully controlled,
        # with a hidden Streamlit button wired up per card via a unique key.
        # The HTML card is purely visual; the real click target is the st.button
        # rendered just below (hidden visually via CSS zero-height wrapper).

        # Build the HTML card grid
        card_html = """
        <div style="
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0;
            border: 1px solid #d8d8d8;
            margin-bottom: 0.1rem;
        ">
        """
        for i, (page_key, page_info) in enumerate(items):
            border_right = "border-right: 1px solid #d8d8d8;" if (i % 3) < 2 and i < len(items) - 1 else ""
            card_html += f"""
            <div style="
                padding: 1.1rem 1rem 1rem;
                background: #f7f7f7;
                {border_right}
            ">
                <p style="
                    font-size: 0.875rem;
                    font-weight: 400;
                    color: #1a1a1a;
                    margin: 0 0 1rem;
                    letter-spacing: 0.01em;
                ">{page_info['label']}</p>
                <p style="
                    font-size: 0.62rem;
                    letter-spacing: 0.16em;
                    text-transform: uppercase;
                    color: #1a1a1a;
                    margin: 0;
                    border-bottom: 1px solid #1a1a1a;
                    display: inline-block;
                    padding-bottom: 1px;
                    cursor: pointer;
                ">Open</p>
            </div>
            """
        card_html += "</div>"
        st.markdown(card_html, unsafe_allow_html=True)

        # Real buttons (invisible — CSS hides them, logic still works via sidebar)
        # We use visible buttons in a tight row so users can actually click
        cols = st.columns(len(items)) if len(items) > 0 else []
        for i, (page_key, page_info) in enumerate(items):
            with cols[i] if isinstance(cols, list) and len(cols) > i else st.container():
                if st.button(f"↗ {page_info['label']}", key=f"home_{page_key}"):
                    st.session_state.current_page = page_key
                    st.rerun()

        st.markdown("<div style='margin-bottom:1.25rem'></div>", unsafe_allow_html=True)

else:
    # ── Dynamic loader ────────────────────────────────────────────────────────
    module_path = None
    for dept_label, pages in NAV.items():
        if current in pages:
            module_path = pages[current]["module"]
            break

    if module_path is None:
        st.error(f"Page '{current}' not found.")
    else:
        try:
            root = os.path.dirname(os.path.abspath(__file__))
            if root not in sys.path:
                sys.path.insert(0, root)
            mod = importlib.import_module(module_path)
            if hasattr(mod, "render"):
                mod.render()
            else:
                st.error(f"`{module_path}` has no `render()` function.")
        except ModuleNotFoundError:
            st.warning(
                f"Module `{module_path}` not found yet. Create the file to activate this page.",
                icon="🚧",
            )
        except Exception as e:
            st.exception(e)
