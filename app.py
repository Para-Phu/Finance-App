import streamlit as st
import streamlit.components.v1 as components
import importlib
import sys
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance - Commercial | App Portfolio",
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

# ── Session state — respect share-link routing on first load ─────────────────
# If the URL contains ?current_page=store_proposal (set by the HTML share link),
# navigate directly to that page instead of showing the home screen.
if "current_page" not in st.session_state:
    page_from_url = st.query_params.get("current_page", "_home")
    # Validate it's a real page key to prevent unexpected behaviour
    all_keys = [k for pages in NAV.values() for k in pages]
    st.session_state.current_page = page_from_url if page_from_url in all_keys else "_home"

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
    st.markdown(
        """
        <div style="border-top:1px solid #1a1a1a;padding-top:1.75rem;margin-bottom:2.75rem;">
            <p style="font-size:0.58rem;letter-spacing:0.2em;text-transform:uppercase;color:#bbb;margin:0 0 0.5rem;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;">Finance - Commercial | App Portfolio</p>
            <p style="font-size:1.5rem;font-weight:400;letter-spacing:0.06em;text-transform:uppercase;color:#1a1a1a;margin:0 0 0.65rem;line-height:1.15;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;">Internal Tools</p>
            <p style="font-size:0.82rem;color:#888;margin:0;max-width:400px;line-height:1.75;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;">A collection of tools for finance, operations, marketing, and property.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Department sections
    for dept_label, pages in NAV.items():
        if dept_label == "Home":
            continue

        items = list(pages.items())
        n = len(items)

        st.markdown(
            f"""<p style="font-size:0.58rem;letter-spacing:0.2em;text-transform:uppercase;color:#bbb;margin:0 0 0.6rem;border-top:1px solid #d8d8d8;padding-top:1.1rem;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;">{dept_label}</p>""",
            unsafe_allow_html=True,
        )

        cols_css = "1fr " * min(n, 3)
        cards_inner = ""
        for i, (page_key, page_info) in enumerate(items):
            is_last_in_row = (i % 3 == 2) or (i == n - 1)
            right_border = "" if is_last_in_row else "border-right:1px solid #d8d8d8;"
            cards_inner += f"""
            <div style="padding:1.1rem 1rem 1.1rem;background:#f7f7f7;{right_border}">
                <p style="font-size:0.875rem;font-weight:400;color:#1a1a1a;margin:0 0 1rem;letter-spacing:0.01em;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;">{page_info['label']}</p>
                <span style="font-size:0.62rem;letter-spacing:0.16em;text-transform:uppercase;color:#1a1a1a;border-bottom:1px solid #1a1a1a;padding-bottom:1px;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;">Open</span>
            </div>
            """

        card_html = f"""
        <div style="display:grid;grid-template-columns:{cols_css};border:1px solid #d8d8d8;margin-bottom:2px;">
            {cards_inner}
        </div>
        """
        components.html(card_html, height=110 if n <= 3 else 220, scrolling=False)

        btn_cols = st.columns(min(n, 3))
        for i, (page_key, page_info) in enumerate(items):
            with btn_cols[i % 3]:
                if st.button(page_info["label"], key=f"home_{page_key}"):
                    st.session_state.current_page = page_key
                    st.rerun()

        st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

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
