import streamlit as st
from datetime import date, datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import (
    get_all_expenses, get_expense_by_id, update_expense,
    delete_expense, get_categories, get_paid_by_names
)

SEMESTERS = ["Sem 1", "Sem 2", "Sem 3", "Sem 4"]


def render():
    st.markdown("## ✏️ Edit / Delete Expenses")
    st.markdown("Search, filter, update, or remove expense records.")
    st.markdown("---")

    # ── Filters ───────────────────────────────────────────────────────────────
    st.markdown("### 🔍 Search & Filter")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        f_search = st.text_input("Search", placeholder="Keyword…", key="ed_search")
    with fc2:
        f_sem = st.selectbox("Semester", ["All"] + SEMESTERS, key="ed_sem")
    with fc3:
        paid_by_opts = ["All"] + get_paid_by_names()
        f_paid = st.selectbox("Paid By", paid_by_opts, key="ed_paid")

    df = get_all_expenses(
        semester=f_sem if f_sem != "All" else None,
        paid_by=f_paid if f_paid != "All" else None,
        search=f_search if f_search else None
    )

    if df.empty:
        st.info("📭 No expenses match the current filters.")
        return

    st.markdown(f"**{len(df)} record(s) found** &nbsp;·&nbsp; Total: ₹{df['amount'].sum():,.2f}", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Expense table with actions ─────────────────────────────────────────────
    categories   = get_categories()
    paid_by_list = get_paid_by_names()

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None
    if "delete_id" not in st.session_state:
        st.session_state.delete_id = None

    # Table header
    hc = st.columns([1, 1.8, 1.5, 1.5, 2.5, 1.5, 1, 1])
    for col, h in zip(hc, ["Date","Semester","Paid By","Category","Description","Amount","Edit","Delete"]):
        col.markdown(f"<div class='th'>{h}</div>", unsafe_allow_html=True)

    for _, row in df.iterrows():
        rid = int(row["id"])
        rc = st.columns([1, 1.8, 1.5, 1.5, 2.5, 1.5, 1, 1])
        rc[0].markdown(f"<div class='td'>{row['date']}</div>", unsafe_allow_html=True)
        rc[1].markdown(f"<div class='td'>{row['semester']}</div>", unsafe_allow_html=True)
        rc[2].markdown(f"<div class='td'>{row['paid_by']}</div>", unsafe_allow_html=True)
        rc[3].markdown(f"<div class='td'>{row['category']}</div>", unsafe_allow_html=True)
        rc[4].markdown(f"<div class='td'>{row['description']}</div>", unsafe_allow_html=True)
        rc[5].markdown(f"<div class='td amt'>₹{row['amount']:,.2f}</div>", unsafe_allow_html=True)

        if rc[6].button("✏️", key=f"edit_{rid}", help="Edit this expense"):
            st.session_state.edit_id = rid
            st.session_state.delete_id = None

        if rc[7].button("🗑️", key=f"del_{rid}", help="Delete this expense"):
            st.session_state.delete_id = rid
            st.session_state.edit_id = None

    st.markdown("---")

    # ── Edit form ─────────────────────────────────────────────────────────────
    if st.session_state.edit_id:
        exp = get_expense_by_id(st.session_state.edit_id)
        if exp:
            st.markdown(f"### ✏️ Editing Expense #{exp['id']}")
            with st.form("edit_form"):
                ec1, ec2 = st.columns(2)
                with ec1:
                    try:
                        dval = datetime.strptime(exp["date"], "%Y-%m-%d").date()
                    except Exception:
                        dval = date.today()
                    new_date = st.date_input("Date", value=dval, key="ef_date")
                with ec2:
                    sem_idx = SEMESTERS.index(exp["semester"]) if exp["semester"] in SEMESTERS else 0
                    new_sem = st.selectbox("Semester", SEMESTERS, index=sem_idx, key="ef_sem")

                ec3, ec4 = st.columns(2)
                with ec3:
                    pb_idx = paid_by_list.index(exp["paid_by"]) if exp["paid_by"] in paid_by_list else 0
                    new_paid = st.selectbox("Paid By", paid_by_list, index=pb_idx, key="ef_paid")
                with ec4:
                    cat_idx = categories.index(exp["category"]) if exp["category"] in categories else 0
                    new_cat = st.selectbox("Category", categories, index=cat_idx, key="ef_cat")

                new_desc = st.text_input("Description", value=exp["description"], key="ef_desc")
                new_amt = st.number_input("Amount (₹)", value=float(exp["amount"]), min_value=0.0, step=100.0, format="%.2f", key="ef_amt")

                bc1, bc2, _ = st.columns([1, 1, 3])
                save_btn   = bc1.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                cancel_btn = bc2.form_submit_button("❌ Cancel", use_container_width=True)

            if save_btn:
                errs = []
                if not new_desc.strip():
                    errs.append("Description cannot be empty.")
                if new_amt <= 0:
                    errs.append("Amount must be > ₹0.")
                if errs:
                    for e in errs:
                        st.error(e)
                else:
                    update_expense(exp["id"], str(new_date), new_sem, new_paid, new_cat, new_desc.strip(), new_amt)
                    st.success("✅ Expense updated successfully!")
                    st.session_state.edit_id = None
                    st.rerun()

            if cancel_btn:
                st.session_state.edit_id = None
                st.rerun()

    # ── Delete confirmation ───────────────────────────────────────────────────
    if st.session_state.delete_id:
        exp = get_expense_by_id(st.session_state.delete_id)
        if exp:
            st.markdown(f"""
            <div class="confirm-box">
                <h4>⚠️ Confirm Deletion</h4>
                <p>You are about to permanently delete:</p>
                <p><strong>{exp['description']}</strong> — ₹{exp['amount']:,.2f} ({exp['semester']}, {exp['paid_by']})</p>
                <p>This action cannot be undone.</p>
            </div>""", unsafe_allow_html=True)

            dc1, dc2, _ = st.columns([1, 1, 4])
            if dc1.button("🗑️ Yes, Delete", type="primary", key="confirm_del", use_container_width=True):
                delete_expense(exp["id"])
                st.success("✅ Expense deleted.")
                st.session_state.delete_id = None
                st.rerun()
            if dc2.button("❌ Cancel", key="cancel_del", use_container_width=True):
                st.session_state.delete_id = None
                st.rerun()
