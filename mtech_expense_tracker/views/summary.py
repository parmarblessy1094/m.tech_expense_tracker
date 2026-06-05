import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import get_summary, get_paid_by_totals, get_semester_totals, get_total

SEMESTERS = ["Sem 1", "Sem 2", "Sem 3", "Sem 4"]


def fmt(amount):
    return f"₹{amount:,.2f}"


def render():
    st.markdown("## 📋 Summary")
    st.markdown("Detailed breakdown of all M.Tech expenses grouped by payer and semester.")
    st.markdown("---")

    df = get_summary()
    if df.empty:
        st.info("📭 No expenses recorded yet.")
        return

    paid_totals = get_paid_by_totals()
    sem_totals  = get_semester_totals()
    grand_total = get_total()

    paid_map = dict(zip(paid_totals["paid_by"], paid_totals["total"]))
    sem_map  = dict(zip(sem_totals["semester"], sem_totals["total"]))

    # ── Grand total header ────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="summary-header">
        <span class="sh-title">M.Tech Expenses — Complete Summary</span>
        <span class="sh-total">Grand Total: {fmt(grand_total)}</span>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filter controls ───────────────────────────────────────────────────────
    fc1, fc2 = st.columns(2)
    with fc1:
        all_payers = sorted(df["paid_by"].unique().tolist())
        sel_payer  = st.selectbox("Filter by Paid By", ["All"] + all_payers, key="sum_payer")
    with fc2:
        sel_sem = st.selectbox("Filter by Semester", ["All"] + SEMESTERS, key="sum_sem")

    filtered = df.copy()
    if sel_payer != "All":
        filtered = filtered[filtered["paid_by"] == sel_payer]
    if sel_sem != "All":
        filtered = filtered[filtered["semester"] == sel_sem]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main summary table per payer ─────────────────────────────────────────
    payers = filtered["paid_by"].unique() if sel_payer == "All" else [sel_payer]

    for payer in payers:
        payer_df = filtered[filtered["paid_by"] == payer]
        if payer_df.empty:
            continue

        payer_total = payer_df["amount"].sum()
        payer_pct   = (payer_total / grand_total * 100) if grand_total else 0

        st.markdown(f"""
        <div class="payer-section-header">
            <span class="payer-name">👤 {payer}</span>
            <span class="payer-total">Total: {fmt(payer_total)} &nbsp;({payer_pct:.1f}%)</span>
        </div>""", unsafe_allow_html=True)

        sems_in_payer = payer_df["semester"].unique()
        for sem in SEMESTERS:
            if sem not in sems_in_payer:
                continue
            sem_rows = payer_df[payer_df["semester"] == sem]
            sem_sub_total = sem_rows["amount"].sum()

            # Table
            table_html = """
            <table class="summary-table">
                <thead>
                    <tr>
                        <th style="width:15%">Paid By</th>
                        <th style="width:12%">Semester</th>
                        <th style="width:40%">Expense</th>
                        <th style="width:15%">Category</th>
                        <th style="width:18%;text-align:right">Amount</th>
                    </tr>
                </thead>
                <tbody>"""

            for _, row in sem_rows.iterrows():
                table_html += f"""
                    <tr>
                        <td>{row['paid_by']}</td>
                        <td><span class="sem-badge">{row['semester']}</span></td>
                        <td>{row['description']}</td>
                        <td><span class="cat-badge">{row['category']}</span></td>
                        <td style="text-align:right;font-weight:600;color:#0F4C81">{fmt(row['amount'])}</td>
                    </tr>"""

            table_html += f"""
                </tbody>
                <tfoot>
                    <tr class="subtotal-row">
                        <td colspan="4" style="text-align:right;font-style:italic">{sem} Subtotal</td>
                        <td style="text-align:right">{fmt(sem_sub_total)}</td>
                    </tr>
                </tfoot>
            </table>"""

            st.markdown(table_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="payer-total-bar">
            <strong>{payer} Total = {fmt(payer_total)}</strong>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Semester-wise summary ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎓 Semester-wise Totals")
    sc = st.columns(len(SEMESTERS))
    for col, sem in zip(sc, SEMESTERS):
        val = sem_map.get(sem, 0)
        pct = (val / grand_total * 100) if grand_total else 0
        with col:
            st.markdown(f"""
            <div class="metric-card metric-sem">
                <div class="metric-label">{sem}</div>
                <div class="metric-value">{fmt(val)}</div>
                <div class="metric-sub">{pct:.1f}% of total</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="grand-total-box">
        <span>🏆 Overall Total</span>
        <span class="gt-amt">{fmt(grand_total)}</span>
    </div>""", unsafe_allow_html=True)
