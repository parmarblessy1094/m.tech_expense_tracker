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
    # ── Page-level CSS ────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* ── Page header ── */
    .ed-page-header {
        background: linear-gradient(135deg, #0F2942 0%, #0F4C81 100%);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .ed-page-header .ph-icon  { font-size: 36px; }
    .ed-page-header .ph-title { font-size: 22px; font-weight: 700; color: #FFFFFF; margin-bottom: 2px; }
    .ed-page-header .ph-sub   { font-size: 13px; color: #93C6E7; }

    /* ── Filter card ── */
    .filter-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 20px;
        box-shadow: 0 2px 12px rgba(15,76,129,0.08);
        border-left: 4px solid #0F4C81;
    }
    .filter-card-title {
        font-size: 13px; font-weight: 700; color: #0F4C81;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px;
    }

    /* ── Results badge ── */
    .results-badge {
        background: #EBF5FB;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 13px;
        color: #0F4C81;
    }
    .results-badge .rb-count { font-weight: 700; font-size: 15px; }
    .results-badge .rb-total { font-weight: 700; color: #2E8B57; font-size: 15px; }

    /* ── Expense table ── */
    .exp-table-wrap {
        background: #FFFFFF;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(15,76,129,0.08);
        margin-bottom: 20px;
    }
    .exp-table-header {
        background: linear-gradient(90deg, #0F2942, #1A5276);
        padding: 12px 16px;
        display: grid;
        grid-template-columns: 90px 80px 110px 120px 1fr 100px 44px 44px;
        gap: 8px;
        align-items: center;
    }
    .exp-table-header span {
        font-size: 10px; font-weight: 700; color: #93C6E7;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .exp-row {
        display: grid;
        grid-template-columns: 90px 80px 110px 120px 1fr 100px 44px 44px;
        gap: 8px;
        align-items: center;
        padding: 11px 16px;
        border-bottom: 1px solid #F0F4F8;
        transition: background 0.15s;
    }
    .exp-row:last-child { border-bottom: none; }
    .exp-row:hover { background: #F8FBFE; }
    .exp-cell { font-size: 12px; color: #333; }
    .exp-cell.date  { color: #666; font-size: 11px; }
    .exp-cell.sem   { }
    .exp-cell.paid  { font-weight: 600; color: #0F4C81; }
    .exp-cell.cat   {  }
    .exp-cell.desc  { color: #444; }
    .exp-cell.amt   { font-weight: 700; color: #0F4C81; font-size: 13px; }

    .sem-pill {
        background: #EBF5FB; color: #0F4C81;
        border-radius: 20px; padding: 2px 8px;
        font-size: 10px; font-weight: 700;
        display: inline-block;
    }
    .cat-pill {
        background: #F0FFF4; color: #2E8B57;
        border-radius: 20px; padding: 2px 8px;
        font-size: 10px; font-weight: 600;
        display: inline-block;
    }

    /* ── Action button cols ── */
    .action-col .stButton > button {
        width: 34px !important; height: 34px !important;
        padding: 0 !important; border-radius: 8px !important;
        font-size: 15px !important; border: none !important;
        display: flex; align-items: center; justify-content: center;
    }

    /* ── Edit form card ── */
    .edit-form-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 24px 26px;
        box-shadow: 0 4px 20px rgba(15,76,129,0.12);
        border-top: 4px solid #0F4C81;
        margin-bottom: 20px;
    }
    .edit-form-title {
        font-size: 16px; font-weight: 700; color: #0F2942;
        margin-bottom: 18px; display: flex; align-items: center; gap: 8px;
    }
    .edit-form-title .badge {
        background: #0F4C81; color: white;
        border-radius: 20px; padding: 2px 10px;
        font-size: 11px; font-weight: 600;
    }

    /* ── Delete confirm card ── */
    .delete-card {
        background: #FFF8F0;
        border: 2px solid #E8A020;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .delete-card .dc-title {
        font-size: 16px; font-weight: 700; color: #B7770D; margin-bottom: 10px;
    }
    .delete-card .dc-item {
        background: white; border-radius: 8px; padding: 12px 16px;
        margin: 10px 0; border-left: 3px solid #E8A020;
    }
    .delete-card .dc-desc  { font-size: 15px; font-weight: 700; color: #333; }
    .delete-card .dc-meta  { font-size: 12px; color: #888; margin-top: 3px; }
    .delete-card .dc-amt   { font-size: 18px; font-weight: 800; color: #E8A020; }
    .delete-card .dc-warn  { font-size: 12px; color: #999; margin-top: 12px; }

    /* Mobile responsive */
    @media (max-width: 768px) {
        .exp-table-header,
        .exp-row {
            grid-template-columns: 1fr;
        }
        .exp-table-header { display: none; }
        .exp-row {
            display: flex; flex-wrap: wrap; gap: 4px;
            padding: 12px 14px;
        }
        .exp-cell { font-size: 12px; }
        .exp-cell.amt { margin-left: auto; }
        .ed-page-header { padding: 16px 18px; }
        .ed-page-header .ph-title { font-size: 18px; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="ed-page-header">
        <span class="ph-icon">✏️</span>
        <div>
            <div class="ph-title">Edit / Delete Expenses</div>
            <div class="ph-sub">Search, filter, update, or remove expense records</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filters ───────────────────────────────────────────────────────────────
    st.markdown('<div class="filter-card"><div class="filter-card-title">🔍 Search & Filter</div>', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        f_search = st.text_input("Search", placeholder="Keyword in description…", key="ed_search", label_visibility="collapsed")
        st.caption("Search keyword")
    with fc2:
        f_sem = st.selectbox("Semester", ["All"] + SEMESTERS, key="ed_sem")
    with fc3:
        paid_by_opts = ["All"] + get_paid_by_names()
        f_paid = st.selectbox("Paid By", paid_by_opts, key="ed_paid")
    st.markdown('</div>', unsafe_allow_html=True)

    df = get_all_expenses(
        semester=f_sem if f_sem != "All" else None,
        paid_by=f_paid if f_paid != "All" else None,
        search=f_search if f_search else None
    )

    if df.empty:
        st.markdown("""
        <div style="text-align:center; padding:40px; background:white; border-radius:12px;
                    box-shadow:0 2px 12px rgba(15,76,129,0.06);">
            <div style="font-size:40px; margin-bottom:12px;">📭</div>
            <div style="font-size:16px; font-weight:700; color:#0F4C81; margin-bottom:6px;">No expenses found</div>
            <div style="font-size:13px; color:#888;">Try adjusting your filters or search term.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Results badge ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="results-badge">
        <span><span class="rb-count">{len(df)}</span> record(s) found</span>
        <span>Total: <span class="rb-total">₹{df['amount'].sum():,.2f}</span></span>
    </div>
    """, unsafe_allow_html=True)

    # ── Session state ─────────────────────────────────────────────────────────
    categories   = get_categories()
    paid_by_list = get_paid_by_names()

    if "edit_id"   not in st.session_state: st.session_state.edit_id   = None
    if "delete_id" not in st.session_state: st.session_state.delete_id = None

    # ── Table header (desktop) ────────────────────────────────────────────────
    st.markdown("""
    <div class="exp-table-wrap">
    <div class="exp-table-header">
        <span>Date</span>
        <span>Sem</span>
        <span>Paid By</span>
        <span>Category</span>
        <span>Description</span>
        <span>Amount</span>
        <span>Edit</span>
        <span>Del</span>
    </div>
    """, unsafe_allow_html=True)

    for _, row in df.iterrows():
        rid = int(row["id"])

        # Row HTML (visual only — action buttons are Streamlit widgets below)
        st.markdown(f"""
        <div class="exp-row">
            <div class="exp-cell date">{row['date']}</div>
            <div class="exp-cell sem"><span class="sem-pill">{row['semester']}</span></div>
            <div class="exp-cell paid">{row['paid_by']}</div>
            <div class="exp-cell cat"><span class="cat-pill">{row['category']}</span></div>
            <div class="exp-cell desc">{row['description']}</div>
            <div class="exp-cell amt">₹{row['amount']:,.2f}</div>
            <div></div>
            <div></div>
        </div>
        """, unsafe_allow_html=True)

        # Actual Streamlit action buttons (overlaid via columns trick)
        # We place them right after each row using a thin column strip
        bc = st.columns([90, 80, 110, 120, 999, 100, 44, 44])
        with bc[6]:
            if st.button("✏️", key=f"edit_{rid}", help="Edit this expense", use_container_width=True):
                st.session_state.edit_id   = rid
                st.session_state.delete_id = None
                st.rerun()
        with bc[7]:
            if st.button("🗑️", key=f"del_{rid}", help="Delete this expense", use_container_width=True):
                st.session_state.delete_id = rid
                st.session_state.edit_id   = None
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)  # close exp-table-wrap

    # ── Edit form ─────────────────────────────────────────────────────────────
    if st.session_state.edit_id:
        exp = get_expense_by_id(st.session_state.edit_id)
        if exp:
            st.markdown(f"""
            <div class="edit-form-card">
                <div class="edit-form-title">
                    ✏️ Editing Expense
                    <span class="badge">#{exp['id']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("edit_form"):
                ec1, ec2 = st.columns(2)
                with ec1:
                    try:
                        dval = datetime.strptime(exp["date"], "%Y-%m-%d").date()
                    except Exception:
                        dval = date.today()
                    new_date = st.date_input("📅 Expense Date", value=dval, key="ef_date")
                with ec2:
                    sem_idx  = SEMESTERS.index(exp["semester"]) if exp["semester"] in SEMESTERS else 0
                    new_sem  = st.selectbox("🎓 Semester", SEMESTERS, index=sem_idx, key="ef_sem")

                ec3, ec4 = st.columns(2)
                with ec3:
                    pb_idx   = paid_by_list.index(exp["paid_by"]) if exp["paid_by"] in paid_by_list else 0
                    new_paid = st.selectbox("👤 Paid By", paid_by_list, index=pb_idx, key="ef_paid")
                with ec4:
                    cat_idx  = categories.index(exp["category"]) if exp["category"] in categories else 0
                    new_cat  = st.selectbox("🏷️ Category", categories, index=cat_idx, key="ef_cat")

                new_desc = st.text_input("📝 Description", value=exp["description"], key="ef_desc")
                new_amt  = st.number_input("💰 Amount (₹)", value=float(exp["amount"]),
                                           min_value=0.0, step=100.0, format="%.2f", key="ef_amt")

                st.markdown("<br>", unsafe_allow_html=True)
                bc1, bc2, _ = st.columns([1.2, 1, 2.8])
                save_btn   = bc1.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                cancel_btn = bc2.form_submit_button("✕ Cancel", use_container_width=True)

            if save_btn:
                errs = []
                if not new_desc.strip():    errs.append("Description cannot be empty.")
                if new_amt <= 0:            errs.append("Amount must be greater than ₹0.")
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
            <div class="delete-card">
                <div class="dc-title">⚠️ Confirm Deletion</div>
                <div class="dc-item">
                    <div class="dc-desc">{exp['description']}</div>
                    <div class="dc-meta">{exp['semester']} &nbsp;·&nbsp; Paid by {exp['paid_by']} &nbsp;·&nbsp; {exp['date']}</div>
                    <div class="dc-amt">₹{exp['amount']:,.2f}</div>
                </div>
                <div class="dc-warn">⚠️ This action is permanent and cannot be undone.</div>
            </div>
            """, unsafe_allow_html=True)

            dc1, dc2, _ = st.columns([1.2, 1, 3.8])
            if dc1.button("🗑️ Yes, Delete", type="primary", key="confirm_del", use_container_width=True):
                delete_expense(exp["id"])
                st.success("✅ Expense deleted successfully.")
                st.session_state.delete_id = None
                st.rerun()
            if dc2.button("✕ Cancel", key="cancel_del", use_container_width=True):
                st.session_state.delete_id = None
                st.rerun()