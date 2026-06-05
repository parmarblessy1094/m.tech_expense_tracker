import streamlit as st
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import add_expense, get_categories, get_paid_by_names

SEMESTERS = ["Sem 1", "Sem 2", "Sem 3", "Sem 4"]


def render():
    st.markdown("## ➕ Add Expense")
    st.markdown("Record a new M.Tech expense entry.")
    st.markdown("---")

    categories  = get_categories()
    paid_by_list = get_paid_by_names()

    with st.form("add_expense_form", clear_on_submit=True):
        st.markdown("### 📝 Expense Details")

        col1, col2 = st.columns(2)
        with col1:
            expense_date = st.date_input(
                "📅 Expense Date",
                value=date.today(),
                max_value=date.today(),
                key="ae_date"
            )
        with col2:
            semester = st.selectbox(
                "🎓 Semester",
                SEMESTERS,
                key="ae_semester"
            )

        col3, col4 = st.columns(2)
        with col3:
            paid_by = st.selectbox(
                "👤 Paid By",
                paid_by_list,
                key="ae_paid_by"
            )
        with col4:
            category = st.selectbox(
                "🏷️ Expense Category",
                categories,
                key="ae_category"
            )

        description = st.text_input(
            "📄 Description",
            placeholder="e.g. Adit Registration Fees, First Semester Tuition...",
            key="ae_desc"
        )

        amount = st.number_input(
            "💰 Amount (₹)",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="ae_amount"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col_btn, col_info = st.columns([1, 2])
        with col_btn:
            submitted = st.form_submit_button(
                "💾 Save Expense",
                use_container_width=True,
                type="primary"
            )

    if submitted:
        # Validation
        errors = []
        if not description.strip():
            errors.append("Description cannot be empty.")
        if amount <= 0:
            errors.append("Amount must be greater than ₹0.")

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            add_expense(
                date=str(expense_date),
                semester=semester,
                paid_by=paid_by,
                category=category,
                description=description.strip(),
                amount=amount
            )
            st.success(f"✅ Expense saved! **{description.strip()}** — ₹{amount:,.2f} ({semester}, {paid_by})")
            st.balloons()

    # ── Tips panel ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
        <div class="tip-card">
            <div class="tip-icon">📌</div>
            <div class="tip-title">Be Descriptive</div>
            <div class="tip-text">Use clear names like "HNGU Tuition Fees Sem 1" for easy tracking.</div>
        </div>""", unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="tip-card">
            <div class="tip-icon">📅</div>
            <div class="tip-title">Use Actual Date</div>
            <div class="tip-text">Enter the date the payment was actually made, not today.</div>
        </div>""", unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="tip-card">
            <div class="tip-icon">🏷️</div>
            <div class="tip-title">Right Category</div>
            <div class="tip-text">Choose the most specific category for better reports.</div>
        </div>""", unsafe_allow_html=True)
