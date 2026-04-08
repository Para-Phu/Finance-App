import streamlit as st
import importlib
import sys
import os

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="My App Portfolio",
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
# Add departments and apps here as you build them.
# "module" is the import path relative to this file.
NAV = {
    "🏠 Home": {
        "_home": {"label": "Overview", "module": None}
    },
    "📊 Finance": {
        "budget_tool":  {"label": "Budget Tool",      "module": "departments.finance.budget_tool"},
        "forecast":     {"label": "Forecast",          "module": "departments.finance.forecast"},
    },
    "⚙️ Operations": {
        "logistics":    {"label": "Logistics Tracker", "module": "departments.ops.logistics"},
    },
    "📣 Marketing": {
        "dashboard":    {"label": "Campaign Dashboard","module": "departments.marketing.dashboard"},
    },
    "🏢 Property": {
    "store_proposal": {"label": "New Store Proposal", "module": "departments.property.store_proposal"},
    },
}

# ── Session state defaults ───────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "_home"

# ── Sidebar nav ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗂️ App Portfolio")
    st.markdown("---")

    for dept_label, pages in NAV.items():
        st.markdown(f"**{dept_label}**")
        for page_key, page_info in pages.items():
            active = st.session_state.current_page == page_key
            btn_label = ("▶ " if active else "  ") + page_info["label"]
            if st.button(btn_label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
        st.markdown("")

    st.markdown("---")
    st.caption("Built with Streamlit")

# ── Router ───────────────────────────────────────────────────────────────────
current = st.session_state.current_page

if current == "_home":
    # ── Home page ────────────────────────────────────────────────────────────
    st.title("App Portfolio")
    st.markdown("Welcome. Use the sidebar to navigate between departments and tools.")
    st.markdown("---")

    for dept_label, pages in NAV.items():
        if dept_label == "🏠 Home":
            continue
        st.subheader(dept_label)
        cols = st.columns(3)
        for i, (page_key, page_info) in enumerate(pages.items()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{page_info['label']}**")
                    st.caption(f"Department: {dept_label}")
                    if st.button("Open →", key=f"home_{page_key}"):
                        st.session_state.current_page = page_key
                        st.rerun()
        st.markdown("")

else:
    # ── Dynamic page loader ───────────────────────────────────────────────────
    # Find the module path for the current page
    module_path = None
    for dept_label, pages in NAV.items():
        if current in pages:
            module_path = pages[current]["module"]
            break

    if module_path is None:
        st.error(f"Page '{current}' not found. Check NAV config in app.py.")
    else:
        try:
            # Add project root to path so imports resolve
            root = os.path.dirname(os.path.abspath(__file__))
            if root not in sys.path:
                sys.path.insert(0, root)

            mod = importlib.import_module(module_path)

            # Each app module must expose a render() function
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

