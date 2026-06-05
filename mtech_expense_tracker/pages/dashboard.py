import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import (
    get_total, get_semester_totals, get_paid_by_totals,
    get_category_totals, get_all_expenses
)

SEMESTERS = ["Sem 1", "Sem 2", "Sem 3", "Sem 4"]
PRIMARY = "#0F4C81"
SUCCESS = "#2E8B57"
ACCENT  = "#E8A020"

def fmt(amount):
    return f"₹{amount:,.2f}"


def render():
    st.markdown("## 📊 Dashboard")
    st.markdown("Real-time overview of your M.Tech expense portfolio.")
    st.markdown("---")

    total      = get_total()
    sem_df     = get_semester_totals()
    paid_df    = get_paid_by_totals()
    cat_df     = get_category_totals()
    all_exp    = get_all_expenses()

    sem_map = {row["semester"]: row["total"] for _, row in sem_df.iterrows()}

    # ── Top KPI row ───────────────────────────────────────────────────────────
    st.markdown("### 💰 Financial Overview")
    c0, c1, c2, c3, c4 = st.columns(5)
    with c0:
        st.markdown(f"""
        <div class="metric-card metric-total">
            <div class="metric-label">GRAND TOTAL</div>
            <div class="metric-value">{fmt(total)}</div>
            <div class="metric-sub">All Semesters Combined</div>
        </div>""", unsafe_allow_html=True)
    for col, sem in zip([c1, c2, c3, c4], SEMESTERS):
        val = sem_map.get(sem, 0)
        pct = (val / total * 100) if total else 0
        with col:
            st.markdown(f"""
            <div class="metric-card metric-sem">
                <div class="metric-label">{sem.upper()}</div>
                <div class="metric-value">{fmt(val)}</div>
                <div class="metric-sub">{pct:.1f}% of total</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Paid By Cards ─────────────────────────────────────────────────────────
    if not paid_df.empty:
        st.markdown("### 👥 Amount Paid By Each Person")
        cols = st.columns(min(len(paid_df), 4))
        colors = ["#0F4C81", "#2E8B57", "#E8A020", "#C0392B", "#8E44AD", "#16A085"]
        for i, (_, row) in enumerate(paid_df.iterrows()):
            pct = (row["total"] / total * 100) if total else 0
            with cols[i % 4]:
                st.markdown(f"""
                <div class="metric-card metric-person" style="border-left-color:{colors[i % len(colors)]};">
                    <div class="metric-label">{row['paid_by']}</div>
                    <div class="metric-value" style="color:{colors[i % len(colors)]};">{fmt(row['total'])}</div>
                    <div class="metric-sub">{pct:.1f}% contribution</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row 1 ──────────────────────────────────────────────────────────
    if not all_exp.empty:
        st.markdown("### 📈 Visual Analytics")
        ch1, ch2 = st.columns(2)

        with ch1:
            st.markdown("#### Semester-wise Distribution")
            if not sem_df.empty:
                fig = px.pie(
                    sem_df, values="total", names="semester",
                    color_discrete_sequence=["#0F4C81","#2E8B57","#E8A020","#C0392B"],
                    hole=0.45
                )
                fig.update_traces(textposition="outside", textinfo="percent+label",
                                  textfont_size=12, marker_line_width=2,
                                  marker_line_color="white")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=True, legend=dict(orientation="h", y=-0.15),
                    margin=dict(t=20, b=60, l=20, r=20), height=360,
                    font=dict(family="Poppins, sans-serif")
                )
                fig.add_annotation(text=f"<b>₹{total/100000:.1f}L</b>", x=0.5, y=0.5,
                                   font_size=18, showarrow=False, font_color=PRIMARY)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data yet.")

        with ch2:
            st.markdown("#### Paid By Contribution")
            if not paid_df.empty:
                fig2 = px.bar(
                    paid_df, x="paid_by", y="total",
                    color="paid_by",
                    color_discrete_sequence=["#0F4C81","#2E8B57","#E8A020","#C0392B","#8E44AD"],
                    text_auto=True
                )
                fig2.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside",
                                   marker_line_width=0)
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    xaxis=dict(title="", showgrid=False),
                    yaxis=dict(title="Amount (₹)", showgrid=True, gridcolor="#E8ECF0"),
                    margin=dict(t=20, b=40, l=20, r=20), height=360,
                    font=dict(family="Poppins, sans-serif")
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No data yet.")

        # ── Charts row 2 ──────────────────────────────────────────────────────
        ch3, ch4 = st.columns(2)

        with ch3:
            st.markdown("#### Category-wise Breakdown")
            if not cat_df.empty:
                fig3 = px.bar(
                    cat_df.sort_values("total"), x="total", y="category",
                    orientation="h",
                    color="total",
                    color_continuous_scale=["#B8D4F0","#0F4C81"],
                    text_auto=True
                )
                fig3.update_traces(texttemplate="₹%{x:,.0f}", textposition="outside")
                fig3.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    coloraxis_showscale=False,
                    xaxis=dict(title="Amount (₹)", showgrid=True, gridcolor="#E8ECF0"),
                    yaxis=dict(title=""),
                    margin=dict(t=20, b=40, l=20, r=20), height=380,
                    font=dict(family="Poppins, sans-serif")
                )
                st.plotly_chart(fig3, use_container_width=True)

        with ch4:
            st.markdown("#### Expense Timeline")
            if not all_exp.empty and "date" in all_exp.columns:
                timeline = all_exp.copy()
                timeline["date"] = pd.to_datetime(timeline["date"], errors="coerce")
                timeline = timeline.dropna(subset=["date"])
                timeline = timeline.sort_values("date")
                timeline["cumulative"] = timeline["amount"].cumsum()
                fig4 = go.Figure()
                fig4.add_trace(go.Scatter(
                    x=timeline["date"], y=timeline["cumulative"],
                    mode="lines+markers",
                    line=dict(color=PRIMARY, width=2),
                    marker=dict(size=6, color=PRIMARY),
                    fill="tozeroy",
                    fillcolor="rgba(15,76,129,0.1)",
                    name="Cumulative"
                ))
                fig4.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(title="Date", showgrid=False),
                    yaxis=dict(title="Cumulative (₹)", showgrid=True, gridcolor="#E8ECF0"),
                    margin=dict(t=20, b=40, l=20, r=20), height=380,
                    showlegend=False,
                    font=dict(family="Poppins, sans-serif")
                )
                st.plotly_chart(fig4, use_container_width=True)

        # ── Recent Transactions ────────────────────────────────────────────────
        st.markdown("### 🕐 Recent Transactions")
        recent = all_exp.head(8).copy()
        if not recent.empty:
            recent["Amount"] = recent["amount"].apply(lambda x: f"₹{x:,.2f}")
            recent["Date"] = recent["date"]
            display = recent[["Date","semester","paid_by","category","description","Amount"]].copy()
            display.columns = ["Date","Semester","Paid By","Category","Description","Amount"]
            display = display.reset_index(drop=True)
            display.index = display.index + 1
            st.dataframe(display, use_container_width=True, height=280)
        else:
            st.info("No expenses recorded yet. Go to **Add Expense** to get started.")
    else:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#999;">
            <h3>📭 No expenses yet</h3>
            <p>Navigate to <strong>Add Expense</strong> from the sidebar to record your first expense.</p>
        </div>""", unsafe_allow_html=True)

import pandas as pd
