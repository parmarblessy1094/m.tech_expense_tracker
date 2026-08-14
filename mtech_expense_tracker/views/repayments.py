import streamlit as st
import pandas as pd
from datetime import date, datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import (
    add_repayment, get_all_repayments, get_repayment_by_id, delete_repayment,
    get_paid_by_names, get_paid_by_totals, get_repayment_totals_by_person,
    get_total, get_total_repaid, get_person_balances
)

def fmt(v):
    return f"₹{v:,.2f}"

# ── colour palette ─────────────────────────────────────────────────────────────
COLORS = ["#0F4C81","#2E8B57","#E8A020","#C0392B","#8E44AD","#16A085"]


def _balance_cards(balances_df):
    """
    Show one card per person who either paid an expense or received a
    repayment (so lenders like 'Jayanti Mama' show up even if every
    expense in the app happens to be logged under 'Self') with:
        Spent  |  Repaid  |  Still Owed
    """
    st.markdown("### 💳 Outstanding Balance per Person")
    if balances_df.empty:
        st.info("No expenses recorded yet.")
        return

    cols = st.columns(min(len(balances_df), 4))
    for i, (_, row) in enumerate(balances_df.iterrows()):
        person   = row["person"]
        spent    = row["spent"]
        repaid   = row["repaid"]
        owed     = row["owed"]
        pct_done = (repaid / spent * 100) if spent else 0
        color    = COLORS[i % len(COLORS)]

        bar_filled = int(pct_done)
        bar_empty  = 100 - bar_filled

        with cols[i % 4]:
            st.markdown(f"""
            <div class="rp-balance-card" style="border-top-color:{color};">
                <div class="rp-person">{person}</div>

                <div class="rp-row">
                    <span class="rp-lbl">Total Spent</span>
                    <span class="rp-val" style="color:{color};">{fmt(spent)}</span>
                </div>
                <div class="rp-row">
                    <span class="rp-lbl">Repaid So Far</span>
                    <span class="rp-val rp-green">{fmt(repaid)}</span>
                </div>
                <div class="rp-row rp-owed-row">
                    <span class="rp-lbl"><b>Still Owed</b></span>
                    <span class="rp-val rp-owed">{"✅ Settled" if owed == 0 else fmt(owed)}</span>
                </div>

                <div class="rp-progress-wrap">
                    <div class="rp-progress-bar" style="width:{pct_done:.1f}%; background:{color};"></div>
                </div>
                <div class="rp-pct">{pct_done:.1f}% repaid</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def render():
    st.markdown("## 💸 Repayments")
    st.markdown("Track money returned to anyone who paid on your behalf — and see exactly what is still owed.")
    st.markdown("---")

    names       = get_paid_by_names()
    balances_df = get_person_balances()      # person, spent, repaid, owed
    total_spent = get_total()
    total_repaid= get_total_repaid()
    net_owed    = max(total_spent - total_repaid, 0)

    # ── CSS for this page ─────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* ── Balance cards ─────────────────────────────── */
    .rp-balance-card {
        background:#fff; border-radius:12px; padding:16px 18px 12px;
        box-shadow:0 2px 12px rgba(15,76,129,0.09); margin-bottom:14px;
        border-top:4px solid #0F4C81;
    }
    .rp-person { font-size:14px; font-weight:700; color:#0F2942; margin-bottom:10px; }
    .rp-row    { display:flex; justify-content:space-between; align-items:center;
                 margin-bottom:5px; font-size:12px; }
    .rp-lbl    { color:#777; }
    .rp-val    { font-weight:600; font-size:13px; }
    .rp-green  { color:#2E8B57 !important; }
    .rp-owed-row { border-top:1px solid #EEE; padding-top:6px; margin-top:4px; }
    .rp-owed   { color:#C0392B !important; font-size:14px !important; }
    .rp-progress-wrap {
        background:#EEE; border-radius:99px; height:6px; margin:10px 0 4px; overflow:hidden;
    }
    .rp-progress-bar  { height:6px; border-radius:99px; transition:width .3s; }
    .rp-pct { font-size:10px; color:#999; text-align:right; }

    /* ── Grand totals strip ─────────────────────────── */
    .rp-strip {
        display:flex; gap:12px; margin-bottom:20px; flex-wrap:wrap;
    }
    .rp-strip-box {
        flex:1; min-width:140px; background:#fff; border-radius:10px;
        padding:14px 16px; box-shadow:0 2px 10px rgba(15,76,129,0.08);
        text-align:center;
    }
    .rp-strip-label { font-size:10px; color:#888; text-transform:uppercase;
                      letter-spacing:.7px; margin-bottom:5px; font-weight:600; }
    .rp-strip-val   { font-size:20px; font-weight:700; }

    /* ── History table ──────────────────────────────── */
    .rp-table { width:100%; border-collapse:collapse; font-size:13px; }
    .rp-table th {
        background:#0F4C81; color:#fff; padding:9px 12px;
        font-weight:600; text-align:left; font-size:12px;
    }
    .rp-table td { padding:9px 12px; border-bottom:1px solid #EEE; color:#333; }
    .rp-table tr:nth-child(even) td { background:#F8FBFE; }
    .rp-table tr:hover td { background:#EBF5FB; }
    .rp-amt  { font-weight:700; color:#2E8B57; text-align:right; }
    .rp-from { font-weight:600; color:#0F4C81; }
    .rp-to   { font-weight:600; color:#C0392B; }

    /* ── Timeline pill ──────────────────────────────── */
    .rp-pill {
        display:inline-block; background:#EBF5FB; color:#0F4C81;
        border-radius:20px; padding:2px 10px; font-size:11px; font-weight:600;
    }

    /* ── Form card ──────────────────────────────────── */
    .rp-form-hint {
        background:linear-gradient(135deg,#EBF5FB,#D6EAF8);
        border-left:4px solid #0F4C81; border-radius:8px;
        padding:12px 16px; font-size:13px; color:#1A5276; margin-bottom:16px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Grand totals strip ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="rp-strip">
        <div class="rp-strip-box">
            <div class="rp-strip-label">Total Expenses</div>
            <div class="rp-strip-val" style="color:#0F4C81;">{fmt(total_spent)}</div>
        </div>
        <div class="rp-strip-box">
            <div class="rp-strip-label">Total Repaid</div>
            <div class="rp-strip-val" style="color:#2E8B57;">{fmt(total_repaid)}</div>
        </div>
        <div class="rp-strip-box">
            <div class="rp-strip-label">Still Outstanding</div>
            <div class="rp-strip-val" style="color:{'#C0392B' if net_owed > 0 else '#2E8B57'};">
                {"✅ All Clear" if net_owed == 0 else fmt(net_owed)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Per-person balance cards ───────────────────────────────────────────────
    _balance_cards(balances_df)
    st.markdown("---")

    # ── Add Repayment form ─────────────────────────────────────────────────────
    st.markdown("### ➕ Record a Repayment")
    st.markdown("""
    <div class="rp-form-hint">
        💡 <b>How it works:</b> Select <i>who</i> paid the money back, and <i>to whom</i> they gave it.
        For example: <b>Self paid ₹5,000 → Jayanti Mama</b> means you returned ₹5,000 to Jayanti Mama.
        This reduces their outstanding amount.
    </div>""", unsafe_allow_html=True)

    with st.form("add_repayment_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            rp_date = st.date_input("📅 Payment Date", value=date.today(),
                                     max_value=date.today(), key="rp_date")
        with c2:
            rp_amount = st.number_input("💰 Amount (₹)", min_value=1.0,
                                         step=100.0, format="%.2f", key="rp_amount")

        c3, c4 = st.columns(2)
        with c3:
            payer_opts = ["Self"] + [n for n in names if n != "Self"]
            rp_paid_by = st.selectbox("👤 Paid By (who gave the money)",
                                       payer_opts, key="rp_paid_by")
        with c4:
            # paid_to = the original lender — exclude the payer themselves
            to_opts = [n for n in names if n != rp_paid_by]
            if not to_opts:
                to_opts = names
            rp_paid_to = st.selectbox("🎯 Paid To (who received it)",
                                       to_opts, key="rp_paid_to")

        rp_note = st.text_input("📝 Note (optional)",
                                  placeholder="e.g. UPI transfer, Cash in hand…",
                                  key="rp_note")

        submitted = st.form_submit_button("💾 Save Repayment",
                                           type="primary", use_container_width=True)

    if submitted:
        errs = []
        if rp_amount <= 0:
            errs.append("Amount must be greater than ₹0.")
        if rp_paid_by == rp_paid_to:
            errs.append("Paid By and Paid To cannot be the same person.")
        if errs:
            for e in errs:
                st.error(f"❌ {e}")
        else:
            add_repayment(str(rp_date), rp_paid_by, rp_paid_to, rp_amount, rp_note.strip())
            st.success(
                f"✅ Repayment saved! **{rp_paid_by}** paid **{fmt(rp_amount)}** to **{rp_paid_to}**"
                + (f" · Note: {rp_note.strip()}" if rp_note.strip() else "")
            )
            st.rerun()

    st.markdown("---")

    # ── Repayment History ──────────────────────────────────────────────────────
    st.markdown("### 📜 Repayment History")

    all_rp = get_all_repayments()

    if all_rp.empty:
        st.info("📭 No repayments recorded yet. Use the form above to add your first entry.")
        return

    # Filter bar
    hf1, hf2, hf3 = st.columns(3)
    with hf1:
        f_from = st.selectbox("Filter: Paid By", ["All"] + names, key="rp_f_from")
    with hf2:
        f_to   = st.selectbox("Filter: Paid To", ["All"] + names, key="rp_f_to")
    with hf3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**{len(all_rp)} record(s)** · Total repaid: **{fmt(all_rp['amount'].sum())}**")

    filt = all_rp.copy()
    if f_from != "All":
        filt = filt[filt["paid_by"] == f_from]
    if f_to != "All":
        filt = filt[filt["paid_to"] == f_to]

    if filt.empty:
        st.info("No repayments match the selected filters.")
        return

    # Init delete state
    if "rp_delete_id" not in st.session_state:
        st.session_state.rp_delete_id = None

    # Build HTML table
    rows_html = ""
    for _, row in filt.iterrows():
        rid      = int(row["id"])
        note_str = row["note"] if row.get("note") else "—"
        rows_html += f"""
        <tr>
            <td><span class="rp-pill">{row['date']}</span></td>
            <td class="rp-from">{row['paid_by']}</td>
            <td style="text-align:center;color:#777;">→</td>
            <td class="rp-to">{row['paid_to']}</td>
            <td class="rp-amt">{fmt(row['amount'])}</td>
            <td style="color:#666;font-size:12px;">{note_str}</td>
            <td>__DELETE_{rid}__</td>
        </tr>"""

    table_html = f"""
    <table class="rp-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Paid By</th>
                <th></th>
                <th>Paid To</th>
                <th style="text-align:right">Amount</th>
                <th>Note</th>
                <th>Delete</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>"""

    # Render table rows + delete buttons side-by-side using columns
    # Header
    hcols = st.columns([2, 2, 0.5, 2, 2, 3, 1])
    for col, lbl in zip(hcols, ["Date","Paid By","","Paid To","Amount","Note","Del"]):
        col.markdown(f"<div class='th'>{lbl}</div>", unsafe_allow_html=True)

    for _, row in filt.iterrows():
        rid      = int(row["id"])
        note_str = str(row["note"]) if row.get("note") else "—"
        rc = st.columns([2, 2, 0.5, 2, 2, 3, 1])
        rc[0].markdown(f"<div class='td'><span class='rp-pill'>{row['date']}</span></div>", unsafe_allow_html=True)
        rc[1].markdown(f"<div class='td rp-from'>{row['paid_by']}</div>", unsafe_allow_html=True)
        rc[2].markdown("<div class='td' style='text-align:center;color:#999;'>→</div>", unsafe_allow_html=True)
        rc[3].markdown(f"<div class='td rp-to'>{row['paid_to']}</div>", unsafe_allow_html=True)
        rc[4].markdown(f"<div class='td amt' style='color:#2E8B57;font-weight:700;'>{fmt(row['amount'])}</div>", unsafe_allow_html=True)
        rc[5].markdown(f"<div class='td' style='font-size:12px;color:#555;'>{note_str}</div>", unsafe_allow_html=True)
        if rc[6].button("🗑️", key=f"rp_del_{rid}", help="Delete this repayment"):
            st.session_state.rp_delete_id = rid

    # Delete confirmation
    if st.session_state.rp_delete_id:
        entry = get_repayment_by_id(st.session_state.rp_delete_id)
        if entry:
            st.markdown("---")
            st.markdown(f"""
            <div class="confirm-box">
                <h4>⚠️ Confirm Delete</h4>
                <p>Delete repayment: <b>{entry['paid_by']}</b> paid <b>{fmt(entry['amount'])}</b>
                   to <b>{entry['paid_to']}</b> on {entry['date']}?</p>
                <p style="color:#C0392B;font-size:12px;">This cannot be undone.</p>
            </div>""", unsafe_allow_html=True)
            dc1, dc2, _ = st.columns([1, 1, 4])
            if dc1.button("🗑️ Yes, Delete", type="primary", key="rp_confirm_del", use_container_width=True):
                delete_repayment(entry["id"])
                st.success("✅ Repayment deleted.")
                st.session_state.rp_delete_id = None
                st.rerun()
            if dc2.button("❌ Cancel", key="rp_cancel_del", use_container_width=True):
                st.session_state.rp_delete_id = None
                st.rerun()
