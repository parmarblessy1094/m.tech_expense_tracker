import streamlit as st
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import (
    get_summary, get_paid_by_totals, get_semester_totals, get_total
)

SEMESTERS = ["Sem 1", "Sem 2", "Sem 3", "Sem 4"]


def fmt(v):
    return f"₹{v:,.2f}"


def render():
    st.markdown("## 🖨️ Printable Report")
    st.markdown("Preview and print a formatted expense report.")
    st.markdown("---")

    df          = get_summary()
    paid_totals = get_paid_by_totals()
    sem_totals  = get_semester_totals()
    grand_total = get_total()

    if df.empty:
        st.info("No expenses recorded yet.")
        return

    paid_map = dict(zip(paid_totals["paid_by"], paid_totals["total"]))
    sem_map  = dict(zip(sem_totals["semester"], sem_totals["total"]))

    # Build HTML report
    now = datetime.now().strftime("%d %B %Y, %I:%M %p")

    rows_html = ""
    for _, row in df.iterrows():
        rows_html += f"""
        <tr>
            <td>{row['date']}</td>
            <td>{row['paid_by']}</td>
            <td>{row['semester']}</td>
            <td>{row['category']}</td>
            <td>{row['description']}</td>
            <td class="amt">₹{row['amount']:,.2f}</td>
        </tr>"""

    sem_rows = ""
    for _, sr in sem_totals.iterrows():
        sem_rows += f"<tr><td>{sr['semester']}</td><td class='amt'>{fmt(sr['total'])}</td></tr>"

    pb_rows = ""
    for _, pr in paid_totals.iterrows():
        pct = (pr['total'] / grand_total * 100) if grand_total else 0
        pb_rows += f"<tr><td>{pr['paid_by']}</td><td class='amt'>{fmt(pr['total'])}</td><td>{pct:.1f}%</td></tr>"

    html = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <title>M.Tech Expense Report</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Poppins',sans-serif; color:#222; background:#fff; }}
        .container {{ max-width:900px; margin:0 auto; padding:24px; }}

        .header {{ background:linear-gradient(135deg,#0F4C81,#1A5276); color:#fff; padding:28px; border-radius:8px; text-align:center; margin-bottom:20px; }}
        .header h1 {{ font-size:24px; font-weight:700; }}
        .header p {{ font-size:11px; color:#BDC3C7; margin-top:4px; }}

        .stats-row {{ display:flex; gap:12px; margin-bottom:20px; }}
        .stat-box {{ flex:1; background:#F5F7FA; border-left:4px solid #0F4C81; padding:12px 16px; border-radius:4px; }}
        .stat-box .label {{ font-size:10px; color:#666; text-transform:uppercase; letter-spacing:0.5px; }}
        .stat-box .value {{ font-size:16px; font-weight:700; color:#0F4C81; }}

        h2 {{ font-size:15px; font-weight:600; color:#0F4C81; margin:20px 0 8px; border-bottom:2px solid #E8ECF0; padding-bottom:4px; }}

        table {{ width:100%; border-collapse:collapse; font-size:11px; margin-bottom:20px; }}
        th {{ background:#0F4C81; color:#fff; padding:8px 10px; text-align:left; font-weight:600; }}
        td {{ padding:7px 10px; border-bottom:1px solid #E8ECF0; vertical-align:top; }}
        tr:nth-child(even) td {{ background:#F5F7FA; }}
        .amt {{ text-align:right; font-weight:600; color:#0F4C81; }}

        .totals-row {{ display:flex; gap:20px; }}
        .totals-row table {{ flex:1; }}

        .grand-total {{ background:#0F4C81; color:#fff; padding:14px 20px; border-radius:6px; display:flex; justify-content:space-between; align-items:center; margin-top:20px; }}
        .grand-total .gt-label {{ font-size:14px; font-weight:600; }}
        .grand-total .gt-value {{ font-size:18px; font-weight:700; }}

        .footer {{ text-align:center; font-size:9px; color:#999; margin-top:24px; padding-top:12px; border-top:1px solid #E8ECF0; }}

        @media print {{
            @page {{ size:A4; margin:1.5cm; }}
            body {{ font-size:10px; }}
            .no-print {{ display:none !important; }}
            .header {{ background:#0F4C81 !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
            th {{ background:#0F4C81 !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
            .grand-total {{ background:#0F4C81 !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
            <h1>🎓 M.Tech Expense Report</h1>
            <p>Generated: {now} &nbsp;·&nbsp; Total Records: {len(df)}</p>
        </div>

        <div class="stats-row">
            {"".join(f'<div class="stat-box"><div class="label">{sem}</div><div class="value">{fmt(sem_map.get(sem,0))}</div></div>' for sem in SEMESTERS)}
        </div>

        <h2>📄 Expense Details</h2>
        <table>
            <thead>
                <tr>
                    <th>Date</th><th>Paid By</th><th>Semester</th>
                    <th>Category</th><th>Description</th><th>Amount (₹)</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>

        <div class="totals-row">
            <div>
                <h2>🎓 Semester Totals</h2>
                <table>
                    <thead><tr><th>Semester</th><th>Total</th></tr></thead>
                    <tbody>{sem_rows}</tbody>
                </table>
            </div>
            <div>
                <h2>👥 Paid By Totals</h2>
                <table>
                    <thead><tr><th>Paid By</th><th>Total</th><th>%</th></tr></thead>
                    <tbody>{pb_rows}</tbody>
                </table>
            </div>
        </div>

        <div class="grand-total">
            <span class="gt-label">🏆 GRAND TOTAL</span>
            <span class="gt-value">{fmt(grand_total)}</span>
        </div>

        <div class="footer">
            M.Tech Expense Tracker &nbsp;·&nbsp; Confidential Report &nbsp;·&nbsp; All amounts in Indian Rupees (₹)
        </div>
    </div>
    </body>
    </html>"""

    # Preview inside Streamlit
    st.markdown(f"""
    <div style="border:1px solid #E0E0E0; border-radius:8px; overflow:hidden; height:600px;">
        <iframe srcdoc='{html.replace("'", "&apos;")}' style="width:100%;height:600px;border:none;"></iframe>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Print button
    print_js = """
    <script>
    function printReport() {
        var frames = document.querySelectorAll('iframe');
        if (frames.length > 0) {
            frames[frames.length-1].contentWindow.print();
        }
    }
    </script>
    <button onclick="printReport()" style="
        background:#0F4C81; color:white; border:none; padding:12px 28px;
        border-radius:6px; font-size:14px; font-weight:600; cursor:pointer;
        display:block; margin:0 auto; font-family:Poppins,sans-serif;
    ">🖨️ Print Report</button>
    """
    st.markdown(print_js, unsafe_allow_html=True)

    # Also provide HTML download
    st.markdown("<br>", unsafe_allow_html=True)
    fname = f"MTech_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    st.download_button(
        "⬇️ Download as HTML",
        data=html.encode("utf-8"),
        file_name=fname,
        mime="text/html",
        use_container_width=False
    )
