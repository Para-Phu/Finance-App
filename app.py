import streamlit as st
import importlib
import sys
import os

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="App Portfolio",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared style injection ───────────────────────────────────────────────────
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "shared", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ── Navigation structure ─────────────────────────────────────────────────────
NAV = {
    "Home": {
        "_home": {"label": "Overview", "module": None}
    },
    "Finance": {
        "budget_tool":  {"label": "Budget Tool",       "module": "departments.finance.budget_tool"},
        "forecast":     {"label": "Forecast",           "module": "departments.finance.forecast"},
    },
    "Operations": {
        "logistics":    {"label": "Logistics Tracker",  "module": "departments.ops.logistics"},
    },
    "Marketing": {
        "dashboard":    {"label": "Campaign Dashboard", "module": "departments.marketing.dashboard"},
    },
    "Property": {
        "store_proposal": {"label": "New Store Proposal", "module": "departments.property.store_proposal"},
    },
}

# ── Session state defaults ───────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "_home"

# ── Sidebar nav ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("App Portfolio")
    st.markdown("---")

    for dept_label, pages in NAV.items():
        st.markdown(f"**{dept_label}**")
        for page_key, page_info in pages.items():
            active = st.session_state.current_page == page_key
            btn_label = page_info["label"]
            btn_type = "secondary" if active else "tertiary"
            if st.button(
                btn_label,
                key=f"nav_{page_key}",
                use_container_width=True,
                type=btn_type,
            ):
                st.session_state.current_page = page_key
                st.rerun()

    st.markdown("---")
    st.caption("Built with Streamlit")

# ── Router ───────────────────────────────────────────────────────────────────
current = st.session_state.current_page

if current == "_home":

    # ── Hero rule + title ────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="
            border-top: 1px solid currentColor;
            padding-top: 1.5rem;
            margin-bottom: 2.5rem;
        ">
            <p style="
                font-size: 0.7rem;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                opacity: 0.5;
                margin: 0 0 0.4rem;
            ">App Portfolio</p>
            <h1 style="
                font-size: 1.3rem !important;
                font-weight: 400 !important;
                letter-spacing: 0.06em !important;
                text-transform: uppercase;
                margin: 0 0 0.6rem;
            ">Internal Tools</h1>
            <p style="
                font-size: 0.85rem;
                opacity: 0.55;
                margin: 0;
                max-width: 420px;
                line-height: 1.7;
            ">A collection of tools for finance, operations, marketing, and property.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Department sections ──────────────────────────────────────────────────
    for dept_label, pages in NAV.items():
        if dept_label == "Home":
            continue

        # Department label
        st.markdown(
            f"""
            <p style="
                font-size: 0.65rem;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                opacity: 0.45;
                margin: 0 0 0;
                border-top: 0.5px solid rgba(128,128,128,0.25);
                padding-top: 1.25rem;
            ">{dept_label}</p>
            """,
            unsafe_allow_html=True,
        )

        # Tool grid — 3 columns
        cols = st.columns(3, gap="small")
        for i, (page_key, page_info) in enumerate(pages.items()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <p style="
                            font-size: 0.875rem;
                            margin: 0 0 0.75rem;
                            font-weight: 400;
                        ">{page_info['label']}</p>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button("Open", key=f"home_{page_key}"):
                        st.session_state.current_page = page_key
                        st.rerun()

        st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

else:
    # ── Dynamic page loader ───────────────────────────────────────────────────
    module_path = None
    for dept_label, pages in NAV.items():
        if current in pages:
            module_path = pages[current]["module"]
            break

    if module_path is None:
        st.error(f"Page '{current}' not found. Check NAV config in app.py.")
    else:
        try:
            root = os.path.dirname(os.path.abspath(__file__))
            if root not in sys.path:
                sys.path.insert(0, root)

            mod = importlib.import_module(module_path)

            if hasattr(mod, "render"):
                mod.render()
            else:
                st.error(
                    f"`{module_path}` has no `render()` function. "
                    "Add `def render(): ...` to this module."
                )
        except ModuleNotFoundError:
            st.warning(
                f"Module `{module_path}` not found yet. "
                "Create the file to activate this page.",
                icon="🚧"
            )
        except Exception as e:
            st.exception(e)
