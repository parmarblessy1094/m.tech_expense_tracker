import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import (
    get_categories, add_category, delete_category,
    get_paid_by_names, add_paid_by, delete_paid_by
)


def render():
    st.markdown("## ⚙️ Settings")
    st.markdown("Manage expense categories and paid-by names.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["🏷️ Expense Categories", "👥 Paid By Names"])

    # ── Categories tab ────────────────────────────────────────────────────────
    with tab1:
        st.markdown("### Current Categories")
        categories = get_categories()
        if categories:
            cc = st.columns(3)
            for i, cat in enumerate(categories):
                with cc[i % 3]:
                    col_a, col_b = st.columns([4, 1])
                    col_a.markdown(f"""
                    <div class="settings-item">
                        <span class="si-icon">🏷️</span> {cat}
                    </div>""", unsafe_allow_html=True)
                    if col_b.button("🗑️", key=f"del_cat_{cat}", help=f"Remove '{cat}'"):
                        delete_category(cat)
                        st.success(f"✅ '{cat}' removed.")
                        st.rerun()
        else:
            st.info("No categories found.")

        st.markdown("---")
        st.markdown("### ➕ Add New Category")
        with st.form("add_cat_form", clear_on_submit=True):
            new_cat = st.text_input("Category Name", placeholder="e.g. Library Fees", key="new_cat_inp")
            submitted = st.form_submit_button("Add Category", type="primary")
        if submitted:
            if not new_cat.strip():
                st.error("Category name cannot be empty.")
            elif add_category(new_cat.strip()):
                st.success(f"✅ '{new_cat.strip()}' added!")
                st.rerun()
            else:
                st.warning(f"⚠️ '{new_cat.strip()}' already exists.")

    # ── Paid By tab ───────────────────────────────────────────────────────────
    with tab2:
        st.markdown("### Current Paid By Names")
        names = get_paid_by_names()
        if names:
            nc = st.columns(3)
            for i, name in enumerate(names):
                with nc[i % 3]:
                    col_a, col_b = st.columns([4, 1])
                    col_a.markdown(f"""
                    <div class="settings-item">
                        <span class="si-icon">👤</span> {name}
                    </div>""", unsafe_allow_html=True)
                    if col_b.button("🗑️", key=f"del_pb_{name}", help=f"Remove '{name}'"):
                        delete_paid_by(name)
                        st.success(f"✅ '{name}' removed.")
                        st.rerun()
        else:
            st.info("No paid-by names found.")

        st.markdown("---")
        st.markdown("### ➕ Add New Paid By Name")
        with st.form("add_pb_form", clear_on_submit=True):
            new_pb = st.text_input("Name", placeholder="e.g. Uncle / Scholarship", key="new_pb_inp")
            submitted2 = st.form_submit_button("Add Name", type="primary")
        if submitted2:
            if not new_pb.strip():
                st.error("Name cannot be empty.")
            elif add_paid_by(new_pb.strip()):
                st.success(f"✅ '{new_pb.strip()}' added!")
                st.rerun()
            else:
                st.warning(f"⚠️ '{new_pb.strip()}' already exists.")

    # ── Info panel ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### ℹ️ Database Info")
    from database.db import get_connection
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) as c FROM expenses").fetchone()["c"]
    conn.close()

    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(f"""
        <div class="metric-card metric-sem">
            <div class="metric-label">TOTAL EXPENSES</div>
            <div class="metric-value">{count}</div>
            <div class="metric-sub">Records in database</div>
        </div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""
        <div class="metric-card metric-sem">
            <div class="metric-label">CATEGORIES</div>
            <div class="metric-value">{len(get_categories())}</div>
            <div class="metric-sub">Active categories</div>
        </div>""", unsafe_allow_html=True)
    with ic3:
        st.markdown(f"""
        <div class="metric-card metric-sem">
            <div class="metric-label">PAID BY NAMES</div>
            <div class="metric-value">{len(get_paid_by_names())}</div>
            <div class="metric-sub">Registered payers</div>
        </div>""", unsafe_allow_html=True)
