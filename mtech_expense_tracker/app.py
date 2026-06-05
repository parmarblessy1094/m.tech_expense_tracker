import streamlit as st
import sys, os

# ── Path setup ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from database.db import init_db

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blessy's M.Tech Expense Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "M.Tech Expense Tracker — Production Ready Edition"
    }
)

# ── Init DB ────────────────────────────────────────────────────────────────────
init_db()

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap');

/* ─── Base ──────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Poppins', 'Inter', sans-serif;
}

/* Hide Streamlit decorations */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── App background ────────────────────────────────────────────────── */
.stApp {
    background: #F5F7FA;
}
.main .block-container {
    padding: 1.5rem 2rem 3rem;
    max-width: 1400px;
}

/* ─── Sidebar ───────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F2942 0%, #0F4C81 60%, #1A5276 100%);
    border-right: none;
    box-shadow: 4px 0 16px rgba(15,76,129,0.15);
}
section[data-testid="stSidebar"] * {
    color: #E8F4FD !important;
}

.sidebar-logo {
    text-align: center;
    padding: 20px 16px 8px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 16px;
}
.sidebar-logo .logo-icon {
    font-size: 48px;
    display: block;
    margin-bottom: 6px;
}
.sidebar-logo .logo-title {
    font-size: 15px;
    font-weight: 700;
    color: #FFFFFF !important;
    line-height: 1.3;
}
.sidebar-logo .logo-sub {
    font-size: 10px;
    color: #93C6E7 !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.nav-section-title {
    font-size: 10px;
    font-weight: 600;
    color: #7FB3D3 !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 12px 16px 4px;
}

section[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    background: transparent;
    border-radius: 8px;
    padding: 10px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #C8DFF0 !important;
    font-size: 14px;
    font-weight: 400;
    border: 1px solid transparent;
    display: block !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(255,255,255,0.08);
    color: #FFFFFF !important;
    border-color: rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-testid*="active"],
section[data-testid="stSidebar"] .stRadio input:checked + label {
    background: rgba(255,255,255,0.14);
    color: #FFFFFF !important;
    border-color: rgba(255,255,255,0.25);
    font-weight: 600;
}

.sidebar-footer {
    text-align: center;
    padding: 16px;
    border-top: 1px solid rgba(255,255,255,0.1);
    font-size: 10px;
    color: #6EA8D0 !important;
}

/* ─── Metric Cards ──────────────────────────────────────────────────── */
.metric-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 2px 12px rgba(15,76,129,0.08);
    margin-bottom: 12px;
    border-top: 4px solid #E0E0E0;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(15,76,129,0.14);
}
.metric-total { border-top-color: #0F4C81; }
.metric-sem   { border-top-color: #2E8B57; }
.metric-person { border-left: 4px solid #0F4C81; border-top: none; border-radius: 8px; }

.metric-label {
    font-size: 10px;
    font-weight: 600;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 22px;
    font-weight: 700;
    color: #0F4C81;
    line-height: 1.1;
    margin-bottom: 4px;
}
.metric-sub {
    font-size: 11px;
    color: #AAA;
}

/* ─── Summary Styles ────────────────────────────────────────────────── */
.summary-header {
    background: linear-gradient(135deg, #0F4C81, #1A6499);
    color: white;
    padding: 18px 24px;
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}
.sh-title { font-size: 16px; font-weight: 700; }
.sh-total  { font-size: 18px; font-weight: 700; }

.payer-section-header {
    background: #EBF5FB;
    border-left: 5px solid #0F4C81;
    padding: 10px 16px;
    border-radius: 0 6px 6px 0;
    display: flex;
    justify-content: space-between;
    margin: 12px 0 8px;
}
.payer-name  { font-weight: 700; font-size: 15px; color: #0F4C81; }
.payer-total { font-weight: 700; font-size: 14px; color: #2E8B57; }

.summary-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-bottom: 4px;
}
.summary-table th {
    background: #1A5276;
    color: white;
    padding: 9px 12px;
    font-weight: 600;
    text-align: left;
    font-size: 12px;
}
.summary-table td {
    padding: 8px 12px;
    border-bottom: 1px solid #EEE;
    color: #333;
}
.summary-table tr:nth-child(even) td { background: #F8FBFE; }
.summary-table tr:hover td { background: #EBF5FB; }
.summary-table tfoot .subtotal-row td {
    background: #D5EBF5;
    font-weight: 700;
    color: #0F4C81;
    padding: 8px 12px;
}

.sem-badge {
    background: #0F4C81;
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}
.cat-badge {
    background: #EBF5FB;
    color: #0F4C81;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
}

.payer-total-bar {
    background: linear-gradient(90deg, #2E8B57, #27AE60);
    color: white;
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 14px;
    text-align: right;
}

.grand-total-box {
    background: linear-gradient(135deg, #0F4C81, #1A6499);
    color: white;
    padding: 18px 24px;
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 18px;
    font-weight: 700;
}
.gt-amt { font-size: 24px; }

/* ─── Report cards ──────────────────────────────────────────────────── */
.report-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(15,76,129,0.08);
    text-align: center;
    margin-bottom: 12px;
    border-top: 4px solid #0F4C81;
}
.rc-icon  { font-size: 40px; margin-bottom: 10px; }
.rc-title { font-size: 16px; font-weight: 700; color: #0F4C81; margin-bottom: 8px; }
.rc-desc  { font-size: 12px; color: #666; }

/* ─── Tips cards ────────────────────────────────────────────────────── */
.tip-card {
    background: white;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(15,76,129,0.06);
    text-align: center;
}
.tip-icon  { font-size: 28px; margin-bottom: 8px; }
.tip-title { font-size: 13px; font-weight: 700; color: #0F4C81; margin-bottom: 6px; }
.tip-text  { font-size: 12px; color: #666; }

/* ─── Edit/Delete table ─────────────────────────────────────────────── */
.th {
    font-weight: 700;
    font-size: 12px;
    color: #0F4C81;
    padding: 8px 4px;
    border-bottom: 2px solid #0F4C81;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.td {
    padding: 8px 4px;
    font-size: 13px;
    border-bottom: 1px solid #EEE;
    color: #333;
}
.td.amt { font-weight: 700; color: #0F4C81; }

.confirm-box {
    background: #FEF9E7;
    border: 2px solid #E8A020;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 12px 0;
}
.confirm-box h4 { color: #B7770D; margin-bottom: 8px; }

/* ─── Settings ──────────────────────────────────────────────────────── */
.settings-item {
    background: white;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    color: #333;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.si-icon { font-size: 16px; }

/* ─── Streamlit component overrides ─────────────────────────────────── */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
    transition: all 0.2s ease;
}
.stButton > button[kind="primary"] {
    background: #0F4C81;
    border-color: #0F4C81;
}
.stButton > button[kind="primary"]:hover {
    background: #1A5E9A;
    border-color: #1A5E9A;
    box-shadow: 0 4px 12px rgba(15,76,129,0.3);
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    border-radius: 8px;
    border: 1.5px solid #D5E8F5;
    font-family: 'Poppins', sans-serif;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #0F4C81;
    box-shadow: 0 0 0 3px rgba(15,76,129,0.12);
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #EBF5FB;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    padding: 8px 20px;
    color: #0F4C81;
}
.stTabs [aria-selected="true"] {
    background: #0F4C81 !important;
    color: white !important;
}

/* Form styling */
[data-testid="stForm"] {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(15,76,129,0.06);
    border: 1px solid #E8ECF0;
}

/* Alerts */
.stSuccess > div {
    border-radius: 8px;
    border-left: 4px solid #2E8B57;
}
.stError > div {
    border-radius: 8px;
    border-left: 4px solid #C0392B;
}

/* Dataframe */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(15,76,129,0.06);
}

/* Divider */
hr {
    border: none;
    border-top: 1.5px solid #E8ECF0;
    margin: 20px 0;
}

/* Headings */
h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif !important;
}
h2 { color: #0F2942; }

/* Spinner */
.stSpinner > div {
    border-top-color: #0F4C81 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────

NAV_ITEMS = {
    "📊 Dashboard":          "dashboard",
    "➕ Add Expense":        "add_expense",
    "✏️ Edit / Delete":      "edit_expense",
    "📋 Summary":            "summary",
    "📁 Reports":            "reports",
    "🖨️ Print Report":       "printable",
    "⚙️ Settings":           "settings",
}

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🎓</span>
        <div class="logo-title">Blessy's M.Tech Expense Tracker</div>
        <div class="logo-sub">Expense Management System</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nav-section-title">Navigation</div>', unsafe_allow_html=True)

    selected = st.radio(
        "Navigation",
        list(NAV_ITEMS.keys()),
        label_visibility="collapsed",
        key="nav_radio"
    )

    # Quick stats
    from database.db import get_total, get_all_expenses
    total = get_total()
    count = len(get_all_expenses())
    st.markdown(f"""
    <div style="margin-top:24px; padding:14px 16px; background:rgba(255,255,255,0.07);
                border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
        <div style="font-size:10px; color:#7FB3D3; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px;">Quick Stats</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="font-size:12px; color:#C8DFF0;">Total Records</span>
            <span style="font-size:13px; font-weight:700; color:#FFFFFF;">{count}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="font-size:12px; color:#C8DFF0;">Grand Total</span>
            <span style="font-size:13px; font-weight:700; color:#76D7A0;">₹{total:,.0f}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-footer">
        Blessy's M.Tech Expense Tracker v1.0<br>Built with ❤️ using Streamlit
    </div>""", unsafe_allow_html=True)

# ── Route to selected page ────────────────────────────────────────────────────
page_key = NAV_ITEMS[selected]

if page_key == "dashboard":
    from pages.dashboard import render
elif page_key == "add_expense":
    from pages.add_expense import render
elif page_key == "edit_expense":
    from pages.edit_expense import render
elif page_key == "summary":
    from pages.summary import render
elif page_key == "reports":
    from pages.reports import render
elif page_key == "printable":
    from pages.printable import render
elif page_key == "settings":
    from pages.settings import render

render()
