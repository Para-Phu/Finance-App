"""
departments/finance/budget_tool.py
───────────────────────────────────
Example Finance app. Rename, extend, or replace with your own logic.

Every app in the portfolio follows the same pattern:
  1. Import shared utilities
  2. Define a render() function — this is what app.py calls
  3. Keep all Streamlit code inside render()
"""

import streamlit as st
import pandas as pd
from shared.utils import page_header, back_button, require_file_upload, section


def render():
    page_header(
        title="Budget Tool",
        description="Upload a spend CSV to analyse actuals vs budget.",
        icon="💰",
    )

    # ── File upload ───────────────────────────────────────────────────────────
    st.markdown("**Expected columns:** `Category`, `Budget`, `Actual`")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded is None:
        # Show a sample so the user knows what format to use
        st.info("Upload a file above to get started. Sample format shown below.")
        sample = pd.DataFrame({
            "Category": ["Salaries", "Software", "Travel", "Marketing"],
            "Budget":   [50000, 8000, 3000, 12000],
            "Actual":   [49200, 9100, 1800, 11500],
        })
        st.dataframe(sample, use_container_width=True, hide_index=True)
        back_button()
        return

    # ── Process uploaded file ─────────────────────────────────────────────────
    try:
        df = pd.read_csv(uploaded)
        required_cols = {"Category", "Budget", "Actual"}
        if not required_cols.issubset(df.columns):
            st.error(f"CSV must contain columns: {required_cols}")
            return
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return

    df["Variance"] = df["Actual"] - df["Budget"]
    df["Variance %"] = (df["Variance"] / df["Budget"] * 100).round(1)

    # ── Summary metrics ───────────────────────────────────────────────────────
    section("Summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Budget",   f"${df['Budget'].sum():,.0f}")
    m2.metric("Total Actual",   f"${df['Actual'].sum():,.0f}")
    variance = df["Variance"].sum()
    m3.metric("Net Variance",   f"${variance:,.0f}", delta=f"{variance:,.0f}")

    # ── Detail table ──────────────────────────────────────────────────────────
    section("Detail")
    st.dataframe(
        df.style.applymap(
            lambda v: "color: red" if isinstance(v, (int, float)) and v > 0 else "color: green",
            subset=["Variance"]
        ),
        use_container_width=True,
        hide_index=True,
    )

    # ── Chart ─────────────────────────────────────────────────────────────────
    section("Budget vs Actual by Category")
    chart_df = df.set_index("Category")[["Budget", "Actual"]]
    st.bar_chart(chart_df)

    back_button()
