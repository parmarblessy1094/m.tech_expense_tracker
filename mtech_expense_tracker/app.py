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
        "About": "Blessy's M.Tech Expense Tracker — Production Ready Edition"
    }
)

# ── Init DB ────────────────────────────────────────────────────────────────────
init_db()

# ── Session state for mobile nav ──────────────────────────────────────────────
if "active_page" not in st.session_state:
    st.session_state.active_page = "dashboard"

# ── Nav items ─────────────────────────────────────────────────────────────────
NAV_ITEMS = {
    "📊 Dashboard":     "dashboard",
    "➕ Add Expense":   "add_expense",
    "✏️ Edit / Delete": "edit_expense",
    "📋 Summary":       "summary",
    "📁 Reports":       "reports",
    "🖨️ Print Report":  "printable",
    "⚙️ Settings":      "settings",
}

# Bottom nav shows 5 primary items; "More" reveals the rest via sidebar
BOTTOM_NAV = [
    {"key": "dashboard",    "icon": "📊", "label": "Dashboard"},
    {"key": "add_expense",  "icon": "➕", "label": "Add"},
    {"key": "summary",      "icon": "📋", "label": "Summary"},
    {"key": "reports",      "icon": "📁", "label": "Reports"},
    {"key": "settings",     "icon": "⚙️", "label": "Settings"},
]

MORE_NAV = [
    {"key": "edit_expense", "icon": "✏️", "label": "Edit / Delete"},
    {"key": "printable",    "icon": "🖨️", "label": "Print Report"},
]

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap');

/* ─── Base ──────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Poppins', 'Inter', sans-serif;
}

/* Hide Streamlit decorations on desktop; keep header on mobile for hamburger */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
.stDeployButton { display: none; }

/* Desktop: hide header entirely */
@media (min-width: 769px) {
    header { visibility: hidden; }
}

/* Mobile: show header so hamburger ☰ is accessible as backup */
@media (max-width: 768px) {
    header { visibility: visible !important; }
    /* shrink the header height */
    header[data-testid="stHeader"] {
        height: 48px !important;
        min-height: 48px !important;
    }
}

/* ─── App background ────────────────────────────────────────────────── */
.stApp { background: #F5F7FA; }

.main .block-container {
    padding: 1.5rem 2rem 3rem;
    max-width: 1400px;
}

/* Mobile: add bottom padding so content isn't hidden behind the nav bar */
@media (max-width: 768px) {
    .main .block-container {
        padding: 0.75rem 0.75rem 90px !important;
    }
}

/* ─── Sidebar (desktop) ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F2942 0%, #0F4C81 60%, #1A5276 100%);
    border-right: none;
    box-shadow: 4px 0 16px rgba(15,76,129,0.15);
}
section[data-testid="stSidebar"] * { color: #E8F4FD !important; }

.sidebar-logo {
    text-align: center;
    padding: 20px 16px 8px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 16px;
}
.sidebar-logo .logo-icon  { font-size: 48px; display: block; margin-bottom: 6px; }
.sidebar-logo .logo-title { font-size: 15px; font-weight: 700; color: #FFFFFF !important; line-height: 1.3; }
.sidebar-logo .logo-sub   { font-size: 10px; color: #93C6E7 !important; letter-spacing: 0.5px; text-transform: uppercase; }

.nav-section-title {
    font-size: 10px; font-weight: 600; color: #7FB3D3 !important;
    letter-spacing: 1.5px; text-transform: uppercase; padding: 12px 16px 4px;
}

section[data-testid="stSidebar"] .stRadio > label { display: none; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex; flex-direction: column; gap: 2px;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    background: transparent; border-radius: 8px; padding: 10px 16px;
    cursor: pointer; transition: all 0.2s ease; color: #C8DFF0 !important;
    font-size: 14px; font-weight: 400; border: 1px solid transparent;
    display: block !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(255,255,255,0.08); color: #FFFFFF !important;
    border-color: rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-testid*="active"],
section[data-testid="stSidebar"] .stRadio input:checked + label {
    background: rgba(255,255,255,0.14); color: #FFFFFF !important;
    border-color: rgba(255,255,255,0.25); font-weight: 600;
}

.sidebar-footer {
    text-align: center; padding: 16px;
    border-top: 1px solid rgba(255,255,255,0.1);
    font-size: 10px; color: #6EA8D0 !important;
}

/* ─── Mobile Top Header Bar ──────────────────────────────────────────── */
.mobile-topbar {
    display: none;
}
@media (max-width: 768px) {
    .mobile-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg, #0F2942, #0F4C81);
        padding: 10px 16px;
        border-radius: 0 0 14px 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(15,76,129,0.25);
    }
    .mobile-topbar .tb-left  { display: flex; align-items: center; gap: 10px; }
    .mobile-topbar .tb-icon  { font-size: 26px; }
    .mobile-topbar .tb-title { font-size: 14px; font-weight: 700; color: #FFFFFF; line-height: 1.2; }
    .mobile-topbar .tb-sub   { font-size: 9px;  color: #93C6E7; letter-spacing: 0.4px; }
    .mobile-topbar .tb-right { text-align: right; }
    .mobile-topbar .tb-total { font-size: 15px; font-weight: 700; color: #76D7A0; }
    .mobile-topbar .tb-tlabel{ font-size: 9px; color: #93C6E7; }
}

/* ─── Mobile Bottom Navigation Bar ─────────────────────────────────── */
/* The actual nav is rendered by Streamlit buttons inside a hidden container */
.mobile-bottom-nav-wrapper {
    display: none;
}
@media (max-width: 768px) {
    .mobile-bottom-nav-wrapper {
        display: block;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        background: #FFFFFF;
        border-top: 1px solid #E0E8F5;
        box-shadow: 0 -4px 20px rgba(15,76,129,0.15);
        padding: 4px 0 env(safe-area-inset-bottom, 4px);
    }
    /* Style the Streamlit columns inside the nav bar */
    .mobile-bottom-nav-wrapper [data-testid="stHorizontalBlock"] {
        gap: 0 !important;
        padding: 0 4px;
    }
    /* Style the nav buttons */
    .mobile-bottom-nav-wrapper .stButton > button {
        width: 100% !important;
        border: none !important;
        background: transparent !important;
        color: #999 !important;
        font-size: 10px !important;
        font-weight: 500 !important;
        padding: 6px 2px !important;
        border-radius: 10px !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        box-shadow: none !important;
        min-height: 54px !important;
    }
    .mobile-bottom-nav-wrapper .stButton > button:hover {
        background: #EBF5FB !important;
        color: #0F4C81 !important;
    }
    /* Active page button highlight */
    .mobile-bottom-nav-wrapper .active-nav .stButton > button {
        background: #EBF5FB !important;
        color: #0F4C81 !important;
        font-weight: 700 !important;
    }
}

/* Hide sidebar on mobile */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] { display: none !important; }
    .main { margin-left: 0 !important; }
    section[data-testid="stSidebarNav"] { display: none !important; }
}

/* ─── More menu modal on mobile ─────────────────────────────────────── */
@media (max-width: 768px) {
    .more-menu-overlay {
        position: fixed; inset: 0; background: rgba(0,0,0,0.4);
        z-index: 9998; display: flex; align-items: flex-end;
    }
    .more-menu-sheet {
        background: white; width: 100%; border-radius: 16px 16px 0 0;
        padding: 20px 16px 32px;
    }
    .more-menu-sheet h4 { font-size: 13px; color: #888; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .more-menu-sheet .stButton > button {
        width: 100% !important; justify-content: flex-start !important;
        gap: 10px !important; font-size: 15px !important; padding: 14px 16px !important;
        border-radius: 10px !important; border: 1px solid #EEE !important;
        background: white !important; color: #0F2942 !important;
        margin-bottom: 8px !important;
    }
}

/* ─── Metric Cards ──────────────────────────────────────────────────── */
.metric-card {
    background: #FFFFFF; border-radius: 12px; padding: 16px 18px;
    box-shadow: 0 2px 12px rgba(15,76,129,0.08); margin-bottom: 12px;
    border-top: 4px solid #E0E0E0;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(15,76,129,0.14); }
.metric-total  { border-top-color: #0F4C81; }
.metric-sem    { border-top-color: #2E8B57; }
.metric-person { border-left: 4px solid #0F4C81; border-top: none; border-radius: 8px; }

.metric-label { font-size: 10px; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.metric-value { font-size: 22px; font-weight: 700; color: #0F4C81; line-height: 1.1; margin-bottom: 4px; }
.metric-sub   { font-size: 11px; color: #AAA; }

@media (max-width: 768px) {
    .metric-value { font-size: 17px; }
    .metric-card  { padding: 12px 14px; }
}

/* ─── Summary Styles ────────────────────────────────────────────────── */
.summary-header {
    background: linear-gradient(135deg, #0F4C81, #1A6499); color: white;
    padding: 18px 24px; border-radius: 10px;
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;
}
@media (max-width: 768px) {
    .summary-header { flex-direction: column; gap: 6px; text-align: center; padding: 14px 16px; }
    .sh-total { font-size: 15px !important; }
}
.sh-title { font-size: 16px; font-weight: 700; }
.sh-total { font-size: 18px; font-weight: 700; }

.payer-section-header {
    background: #EBF5FB; border-left: 5px solid #0F4C81;
    padding: 10px 16px; border-radius: 0 6px 6px 0;
    display: flex; justify-content: space-between; margin: 12px 0 8px;
}
@media (max-width: 768px) {
    .payer-section-header { flex-direction: column; gap: 2px; }
}
.payer-name  { font-weight: 700; font-size: 15px; color: #0F4C81; }
.payer-total { font-weight: 700; font-size: 14px; color: #2E8B57; }

.summary-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 4px; }
.summary-table th { background: #1A5276; color: white; padding: 9px 12px; font-weight: 600; text-align: left; font-size: 12px; }
.summary-table td { padding: 8px 12px; border-bottom: 1px solid #EEE; color: #333; }
.summary-table tr:nth-child(even) td { background: #F8FBFE; }
.summary-table tr:hover td { background: #EBF5FB; }
.summary-table tfoot .subtotal-row td { background: #D5EBF5; font-weight: 700; color: #0F4C81; padding: 8px 12px; }
@media (max-width: 768px) {
    .summary-table { font-size: 11px; }
    .summary-table th, .summary-table td { padding: 6px 8px; }
}

.sem-badge { background: #0F4C81; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }
.cat-badge { background: #EBF5FB; color: #0F4C81; padding: 2px 8px; border-radius: 12px; font-size: 11px; }

.payer-total-bar { background: linear-gradient(90deg, #2E8B57, #27AE60); color: white; padding: 10px 20px; border-radius: 6px; font-size: 14px; text-align: right; }

.grand-total-box {
    background: linear-gradient(135deg, #0F4C81, #1A6499); color: white;
    padding: 18px 24px; border-radius: 10px;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 18px; font-weight: 700;
}
.gt-amt { font-size: 24px; }
@media (max-width: 768px) {
    .grand-total-box { padding: 14px 16px; font-size: 14px; }
    .gt-amt { font-size: 18px; }
}

/* ─── Report cards ──────────────────────────────────────────────────── */
.report-card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 12px rgba(15,76,129,0.08); text-align: center; margin-bottom: 12px; border-top: 4px solid #0F4C81; }
.rc-icon  { font-size: 40px; margin-bottom: 10px; }
.rc-title { font-size: 16px; font-weight: 700; color: #0F4C81; margin-bottom: 8px; }
.rc-desc  { font-size: 12px; color: #666; }

/* ─── Tips cards ────────────────────────────────────────────────────── */
.tip-card { background: white; border-radius: 10px; padding: 16px; box-shadow: 0 2px 8px rgba(15,76,129,0.06); text-align: center; }
.tip-icon  { font-size: 28px; margin-bottom: 8px; }
.tip-title { font-size: 13px; font-weight: 700; color: #0F4C81; margin-bottom: 6px; }
.tip-text  { font-size: 12px; color: #666; }

/* ─── Edit/Delete table ─────────────────────────────────────────────── */
.th { font-weight: 700; font-size: 12px; color: #0F4C81; padding: 8px 4px; border-bottom: 2px solid #0F4C81; text-transform: uppercase; letter-spacing: 0.5px; }
.td { padding: 8px 4px; font-size: 13px; border-bottom: 1px solid #EEE; color: #333; }
.td.amt { font-weight: 700; color: #0F4C81; }

.confirm-box { background: #FEF9E7; border: 2px solid #E8A020; border-radius: 8px; padding: 16px 20px; margin: 12px 0; }
.confirm-box h4 { color: #B7770D; margin-bottom: 8px; }

/* ─── Settings ──────────────────────────────────────────────────────── */
.settings-item { background: white; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #333; box-shadow: 0 1px 6px rgba(0,0,0,0.06); margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.si-icon { font-size: 16px; }

/* ─── Streamlit component overrides ─────────────────────────────────── */
.stButton > button { border-radius: 8px; font-weight: 600; font-family: 'Poppins', sans-serif; transition: all 0.2s ease; }
.stButton > button[kind="primary"] { background: #0F4C81; border-color: #0F4C81; }
.stButton > button[kind="primary"]:hover { background: #1A5E9A; border-color: #1A5E9A; box-shadow: 0 4px 12px rgba(15,76,129,0.3); }

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    border-radius: 8px; border: 1.5px solid #D5E8F5;
    font-family: 'Poppins', sans-serif; transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #0F4C81; box-shadow: 0 0 0 3px rgba(15,76,129,0.12);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #EBF5FB; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 600; font-size: 14px; padding: 8px 20px; color: #0F4C81; }
.stTabs [aria-selected="true"] { background: #0F4C81 !important; color: white !important; }
@media (max-width: 768px) {
    .stTabs [data-baseweb="tab"] { font-size: 12px; padding: 6px 10px; }
}

/* Form */
[data-testid="stForm"] { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 12px rgba(15,76,129,0.06); border: 1px solid #E8ECF0; }
@media (max-width: 768px) { [data-testid="stForm"] { padding: 14px; } }

/* Alerts */
.stSuccess > div { border-radius: 8px; border-left: 4px solid #2E8B57; }
.stError   > div { border-radius: 8px; border-left: 4px solid #C0392B; }

/* Dataframe */
.stDataFrame { border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(15,76,129,0.06); }

/* Divider */
hr { border: none; border-top: 1.5px solid #E8ECF0; margin: 20px 0; }

/* Headings */
h1, h2, h3, h4 { font-family: 'Poppins', sans-serif !important; }
h2 { color: #0F2942; }
@media (max-width: 768px) {
    h2 { font-size: 1.2rem !important; }
    h3 { font-size: 1rem !important; }
}

/* Spinner */
.stSpinner > div { border-top-color: #0F4C81 !important; }

/* Mobile: hide columns gap overflow */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] { gap: 6px !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar (desktop) ─────────────────────────────────────────────────────────
from database.db import get_total, get_all_expenses
total = get_total()
count = len(get_all_expenses())

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🎓</span>
        <div class="logo-title">Blessy's M.Tech<br>Expense Tracker</div>
        <div class="logo-sub">Expense Management System</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nav-section-title">Navigation</div>', unsafe_allow_html=True)

    nav_labels = list(NAV_ITEMS.keys())
    current_label = next((k for k, v in NAV_ITEMS.items() if v == st.session_state.active_page), nav_labels[0])
    current_index = nav_labels.index(current_label)

    selected_label = st.radio(
        "Navigation",
        nav_labels,
        index=current_index,
        label_visibility="collapsed",
        key="nav_radio"
    )
    # Sync sidebar selection → session state
    st.session_state.active_page = NAV_ITEMS[selected_label]

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

# ── Mobile top header ─────────────────────────────────────────────────────────
st.markdown(f"""
<div class="mobile-topbar">
    <div class="tb-left">
        <span class="tb-icon">🎓</span>
        <div>
            <div class="tb-title">Blessy's M.Tech Tracker</div>
            <div class="tb-sub">Expense Management System</div>
        </div>
    </div>
    <div class="tb-right">
        <div class="tb-total">₹{total:,.0f}</div>
        <div class="tb-tlabel">Grand Total</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── Mobile "More" submenu toggle ──────────────────────────────────────────────
if "show_more_menu" not in st.session_state:
    st.session_state.show_more_menu = False

# ── Mobile bottom navigation (Streamlit buttons — reliable on mobile) ─────────
active_page = st.session_state.active_page

# Inject wrapper div for CSS targeting
st.markdown('<div class="mobile-bottom-nav-wrapper">', unsafe_allow_html=True)

nav_cols = st.columns(len(BOTTOM_NAV) + 1)  # +1 for "More"

for i, item in enumerate(BOTTOM_NAV):
    with nav_cols[i]:
        label = f"{item['icon']}\n{item['label']}"
        if st.button(label, key=f"mob_nav_{item['key']}", use_container_width=True):
            st.session_state.active_page = item["key"]
            st.session_state.show_more_menu = False
            st.rerun()

# "More" button
with nav_cols[-1]:
    more_icon = "✕" if st.session_state.show_more_menu else "☰"
    if st.button(f"{more_icon}\nMore", key="mob_nav_more", use_container_width=True):
        st.session_state.show_more_menu = not st.session_state.show_more_menu
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── More submenu (Edit/Delete, Print) ────────────────────────────────────────
if st.session_state.show_more_menu:
    st.markdown("---")
    st.markdown("**More options:**")
    more_cols = st.columns(len(MORE_NAV))
    for i, item in enumerate(MORE_NAV):
        with more_cols[i]:
            if st.button(f"{item['icon']} {item['label']}", key=f"more_nav_{item['key']}", use_container_width=True):
                st.session_state.active_page = item["key"]
                st.session_state.show_more_menu = False
                st.rerun()
    st.markdown("---")

# ── Route to selected page ────────────────────────────────────────────────────
page_key = st.session_state.active_page

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
