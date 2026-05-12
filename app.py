#  SUPERSTORE SALES — INTERACTIVE STREAMLIT DASHBOARD
#  Course Project | Data Analytics
#  Author : Vivek Pant
#
#  HOW TO RUN:
#      pip install streamlit plotly pandas openpyxl
#      streamlit run app.py
#
#  This opens a browser at http://localhost:8501
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Superstore Sales EDA",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS  —  full design system
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

.stApp {
    background: #F0F4F8;
}

/* Force all main content text black */
.stApp p, .stApp span, .stApp label, .stApp div,
.stApp .stMarkdown, .stApp .stMarkdown p {
    color: #111827;
}

/* ─────────────────────────────
   SIDEBAR
───────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0F2057 0%, #1E3A8A 50%, #1D4ED8 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.2);
    min-width: 270px !important;
    max-width: 320px !important;
}

/* Inner scrollable content area — Streamlit 1.55+ uses stSidebarUserContent */
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarContent"],
section[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding-top: 1rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.3) transparent;
}

[data-testid="stSidebarUserContent"]::-webkit-scrollbar,
[data-testid="stSidebarContent"]::-webkit-scrollbar,
section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
    width: 4px;
}
[data-testid="stSidebarUserContent"]::-webkit-scrollbar-thumb,
[data-testid="stSidebarContent"]::-webkit-scrollbar-thumb,
section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.3);
    border-radius: 4px;
}

/* Force ALL sidebar text white */
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stMarkdown p {
    color: white !important;
}

/* Radio button pills */
section[data-testid="stSidebar"] .stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    cursor: pointer;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease;
    display: flex !important;
    align-items: center;
    margin: 0 !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.18) !important;
    border-color: rgba(255,255,255,0.35) !important;
    transform: translateX(3px);
}

/* Selected radio state */
section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
    background: rgba(255,255,255,0.22) !important;
    border-color: rgba(255,255,255,0.6) !important;
    font-weight: 700 !important;
}

/* Hide the actual radio dot */
section[data-testid="stSidebar"] .stRadio input[type="radio"] {
    display: none !important;
}

/* MultiSelect / Selectbox in sidebar */
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"],
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.25) !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] .stMultiSelect span,
section[data-testid="stSidebar"] .stMultiSelect div,
section[data-testid="stSidebar"] .stSelectbox span,
section[data-testid="stSidebar"] .stSelectbox div {
    color: white !important;
}

/* Sidebar tag chips */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(255,255,255,0.22) !important;
    border-color: rgba(255,255,255,0.35) !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: white !important;
}

/* Date input in sidebar */
section[data-testid="stSidebar"] .stDateInput input {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.25) !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Text input in sidebar */
section[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.25) !important;
    color: white !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: rgba(255,255,255,0.5) !important;
}

/* Divider */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
    margin: 10px 0;
}

/* Sidebar logo box */
.sidebar-logo {
    background: rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 18px 16px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.2);
    text-align: center;
    backdrop-filter: blur(10px);
}

/* ── Force sidebar ALWAYS visible — never collapsed ── */

/* Keep the sidebar element always shown at full width */
section[data-testid="stSidebar"] {
    transform: none !important;
    width: 280px !important;
    min-width: 270px !important;
    max-width: 320px !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
}

/* Override Streamlit's collapsed state that hides the sidebar */
[data-testid="stSidebar"][aria-expanded="false"] {
    transform: none !important;
    width: 280px !important;
    min-width: 270px !important;
    display: block !important;
    visibility: visible !important;
    margin-left: 0 !important;
}

/* Hide the collapse toggle button so users can't close the sidebar */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

/* Keep the main content area from overlapping the sidebar */
.main .block-container,
[data-testid="stMainBlockContainer"] {
    margin-left: 0 !important;
}

/* ─────────────────────────────
   KPI CARDS
───────────────────────────── */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.04);
    border-left: 4px solid #2563EB;
    transition: all 0.25s ease;
    min-height: 100px;
    height: 100%;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.12);
}

.kpi-label { font-size: 10px; color: #9CA3AF; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }
.kpi-value { font-size: 26px; font-weight: 800; color: #111827; margin: 4px 0; }
.kpi-sub   { font-size: 11px; color: #6B7280; margin-top: 4px; }

/* ─────────────────────────────
   CHART CARDS
───────────────────────────── */
.chart-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
}

/* ─────────────────────────────
   INSIGHT BOX
───────────────────────────── */
.insight-box {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border-left: 4px solid #2563EB;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    font-size: 13px;
    color: #111827 !important;
    margin-bottom: 16px;
}

/* ─────────────────────────────
   RECOMMENDATION CARDS
───────────────────────────── */
.rec-card {
    background: white;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #2563EB;
    transition: all 0.25s ease;
}

.rec-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.10);
}

.rec-title {
    font-size: 15px;
    font-weight: 700;
    color: #1E3A8A;
    margin-bottom: 8px;
}

.rec-body {
    font-size: 13px;
    color: #374151;
    line-height: 1.6;
}

/* ─────────────────────────────
   STAT BOX
───────────────────────────── */
.stat-box {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}
.stat-box-title {
    font-size: 11px;
    font-weight: 700;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    color: #374151;
    padding: 3px 0;
    border-bottom: 1px solid #F3F4F6;
}
.stat-row:last-child { border-bottom: none; }
.stat-row strong { color: #111827; font-weight: 600; }

/* ─────────────────────────────
   TABLE & METRICS
───────────────────────────── */
[data-testid="stDataFrame"],
[data-testid="stMetric"] {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    padding: 8px;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
}

[data-testid="stMetricLabel"] {
    color: #6B7280 !important;
}

/* ─────────────────────────────
   HEADINGS
───────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: #111827 !important;
}

.section-header {
    font-size: 22px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 18px;
}

/* Download button */
.stDownloadButton button {
    background: linear-gradient(135deg, #2563EB, #1E3A8A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.4) !important;
}

/* ─────────────────────────────
   PLOTLY CHARTS — force black labels
───────────────────────────── */
.js-plotly-plot .plotly .xtick text,
.js-plotly-plot .plotly .ytick text,
.js-plotly-plot .plotly .g-xtitle text,
.js-plotly-plot .plotly .g-ytitle text,
.js-plotly-plot .plotly .legendtext,
.js-plotly-plot .plotly .annotation-text {
    fill: #111827 !important;
}

/* Hide Plotly "undefined" root label in treemap/sunburst */
.js-plotly-plot .plotly g.slice text[style*="undefined"],
.js-plotly-plot .plotly .slicetext:empty,
g.slice > text.slicetext[data-unformatted=""],
g.trace.treemap text[data-unformatted=""] {
    display: none !important;
}

/* ─────────────────────────────
   HIDE STREAMLIT CHROME
───────────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }

/* ─────────────────────────────
   RESPONSIVE
───────────────────────────── */
@media (max-width: 768px) {
    .kpi-card { padding: 14px 16px; min-height: auto; }
    .kpi-value { font-size: 20px; }
    .kpi-label { font-size: 9px; }
    .section-header { font-size: 18px; }
    .rec-card { padding: 14px 16px; }
    .insight-box { font-size: 12px; padding: 10px 14px; }
    section[data-testid="stSidebar"] { min-width: 220px !important; }
}

@media (max-width: 480px) {
    .kpi-value { font-size: 16px; }
    .kpi-card { padding: 10px 12px; }
    .section-header { font-size: 16px; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# BACKEND — DATA LOADING & CLEANING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and preprocess the Superstore dataset. Returns (df, error_msg)."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(base_dir, "train.csv"),
            "train.csv",
            os.path.join(base_dir, "data", "train.csv"),
            os.path.join(os.getcwd(), "train.csv"),
        ]

        df = None
        for path in possible_paths:
            if os.path.exists(path):
                df = pd.read_csv(path, encoding="utf-8")
                break

        if df is None:
            return None, "train.csv not found. Place it in the same folder as app.py."

        # Try multiple date formats robustly
        for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"):
            try:
                df["Order Date"] = pd.to_datetime(df["Order Date"], format=fmt, errors="raise")
                df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format=fmt, errors="raise")
                break
            except Exception:
                continue
        else:
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
            df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  errors="coerce")

        df = df.dropna(subset=["Order Date", "Ship Date"])

        if "Postal Code" in df.columns:
            df["Postal Code"] = df["Postal Code"].fillna(0).astype(int)

        # Derived columns
        df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)
        df["Year"]       = df["Order Date"].dt.year
        df["Month Name"] = df["Order Date"].dt.strftime("%b")
        df["Month Num"]  = df["Order Date"].dt.month
        df["Quarter"]    = "Q" + df["Order Date"].dt.quarter.astype(str)
        df["Ship Days"]  = (df["Ship Date"] - df["Order Date"]).dt.days
        df["Ship Days"]  = df["Ship Days"].clip(lower=0)

        return df, None

    except Exception as e:
        return None, str(e)


# Load data — errors handled outside cache so st calls work fine
df, load_err = load_data()
if load_err or df is None or len(df) == 0:
    st.error(f"❌ Could not load data: {load_err or 'Dataset is empty.'}")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Navigation + Filters
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:32px;">🛒</div>
        <div style="font-size:17px; font-weight:800; margin-top:6px;">Superstore EDA</div>
        <div style="font-size:11px; opacity:0.75; margin-top:3px;">Data Analytics Project</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio("📍 Navigate to", [
        "🏠  Overview",
        "📈  Trend Analysis",
        "📦  Category Analysis",
        "👥  Customer Segments",
        "🗺️  Geospatial Analysis",
        "🚚  Shipping Analysis",
        "💡  Business Insights",
    ], label_visibility="visible")

    st.markdown("---")
    st.markdown("### 🔧 Filters")

    # Year & Region
    years = sorted(df["Year"].unique())
    regions = sorted(df["Region"].unique())
    categories = sorted(df["Category"].unique())
    segments = sorted(df["Segment"].unique())

    selected_years   = st.multiselect("Year", years, default=years)
    selected_regions = st.multiselect("Region", regions, default=regions)
    selected_cats    = st.multiselect("Category", categories, default=categories)
    selected_segs    = st.multiselect("Segment", segments, default=segments)

    # Date range filter  ───────────────────────────────────────────────────────
    st.markdown("**Date Range**")
    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    _from = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date, key="date_from")
    _to   = st.date_input("To",   value=max_date, min_value=min_date, max_value=max_date, key="date_to")
    # Streamlit 1.35+ can return None if cleared, or a tuple for range pickers
    # Normalise to a single datetime.date in all cases
    def _safe_date(val, fallback):
        if val is None:
            return fallback
        if isinstance(val, (list, tuple)):
            return val[0] if len(val) > 0 else fallback
        return val
    date_from = _safe_date(_from, min_date)
    date_to   = _safe_date(_to,   max_date)

    # Customer search  ─────────────────────────────────────────────────────────
    cust_search = st.text_input("🔍 Customer search", placeholder="e.g. Claire")

    st.markdown("---")
    st.markdown("**Team:** Vivek · Yash · Param · Harishta")
    st.markdown(f"**Dataset:** {len(df):,} orders")
    st.markdown(f"**Period:** {df['Year'].min()} – {df['Year'].max()}")


# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
sel_years   = selected_years   or years
sel_regions = selected_regions or regions
sel_cats    = selected_cats    or categories
sel_segs    = selected_segs    or segments

# Guard: date_from must be ≤ date_to
if date_from > date_to:
    date_from, date_to = date_to, date_from

try:
    fdf = df[
        df["Year"].isin(sel_years) &
        df["Region"].isin(sel_regions) &
        df["Category"].isin(sel_cats) &
        df["Segment"].isin(sel_segs) &
        (df["Order Date"].dt.date >= date_from) &
        (df["Order Date"].dt.date <= date_to)
    ].copy()

    if cust_search.strip():
        fdf = fdf[fdf["Customer Name"].str.contains(cust_search.strip(), case=False, na=False)]

    if len(fdf) == 0:
        st.warning("⚠️ No data matches your current filters. Showing all data instead.")
        fdf = df.copy()

except Exception as e:
    st.error(f"Error applying filters: {e}")
    fdf = df.copy()


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def kpi(label, value, sub="", color="#2563EB"):
    return f"""<div class="kpi-card" style="border-left-color:{color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

def download_csv(df_to_dl, label="⬇️ Download Filtered Data"):
    """Render a CSV download button for the given DataFrame."""
    buf = io.BytesIO()
    df_to_dl.to_csv(buf, index=False)
    st.download_button(
        label=label,
        data=buf.getvalue(),
        file_name="superstore_filtered.csv",
        mime="text/csv",
    )

BLACK_FONT = dict(color="black")
AXIS_STYLE = dict(tickfont=BLACK_FONT, title_font=BLACK_FONT, color="black")

_BASE_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=0, r=0, t=30, b=0),
    font=dict(family="Inter, Segoe UI, sans-serif", color="black"),
    legend=dict(font=BLACK_FONT, title_font=BLACK_FONT),
    title_font=BLACK_FONT,
)

def chart_layout(**overrides):
    layout = dict(_BASE_LAYOUT)
    layout["xaxis"] = {**AXIS_STYLE, **overrides.pop("xaxis", {})}
    layout["yaxis"] = {**AXIS_STYLE, **overrides.pop("yaxis", {})}
    layout.update(overrides)
    return layout

CAT_COLORS  = {"Furniture": "#10B981", "Office Supplies": "#F59E0B", "Technology": "#2563EB"}
REG_COLORS  = {"West": "#2563EB", "East": "#10B981", "Central": "#F59E0B", "South": "#EF4444"}
SEG_COLORS  = {"Consumer": "#2563EB", "Corporate": "#10B981", "Home Office": "#F59E0B"}
SHIP_COLORS = {
    "Standard Class": "#2563EB",
    "Second Class":   "#10B981",
    "First Class":    "#F59E0B",
    "Same Day":       "#EF4444",
}


# =============================================================================
# PAGE 1 — OVERVIEW
# =============================================================================
if page == "🏠  Overview":
    st.markdown('<div class="section-header">🏠 Project Overview Dashboard</div>', unsafe_allow_html=True)

    # ── KPI row ──────────────────────────────────────────────────────────────
    total_sales  = fdf["Sales"].sum()
    total_orders = len(fdf)
    avg_order    = fdf["Sales"].mean() if total_orders > 0 else 0
    unique_custs = fdf["Customer Name"].nunique()
    unique_prods = fdf["Product Name"].nunique()

    try:
        top_state = fdf.groupby("State")["Sales"].sum().idxmax()
    except Exception:
        top_state = "N/A"

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi("Total Revenue",     f"${total_sales:,.0f}",  "All filtered orders",   "#2563EB"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Orders",       f"{total_orders:,}",    "Transactions",          "#10B981"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Avg Order Value",    f"${avg_order:,.0f}",   "Per transaction",       "#F59E0B"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Unique Customers",   f"{unique_custs:,}",    "Individual buyers",     "#8B5CF6"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("Products Sold",      f"{unique_prods:,}",    f"Top state: {top_state}","#EF4444"), unsafe_allow_html=True)

    st.markdown("---")

    # ── Summary statistics ───────────────────────────────────────────────────
    with st.expander("📊 Sales Distribution Summary", expanded=False):
        s = fdf["Sales"]
        stat_cols = st.columns(4)
        with stat_cols[0]:
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-box-title'>Central Tendency</div>
                <div class='stat-row'><span>Mean</span><strong>${s.mean():,.2f}</strong></div>
                <div class='stat-row'><span>Median</span><strong>${s.median():,.2f}</strong></div>
                <div class='stat-row'><span>Mode (approx)</span><strong>${s.mode().iloc[0]:,.2f}</strong></div>
            </div>""", unsafe_allow_html=True)
        with stat_cols[1]:
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-box-title'>Spread</div>
                <div class='stat-row'><span>Std Dev</span><strong>${s.std():,.2f}</strong></div>
                <div class='stat-row'><span>Variance</span><strong>${s.var():,.0f}</strong></div>
                <div class='stat-row'><span>IQR</span><strong>${s.quantile(0.75)-s.quantile(0.25):,.2f}</strong></div>
            </div>""", unsafe_allow_html=True)
        with stat_cols[2]:
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-box-title'>Range</div>
                <div class='stat-row'><span>Min</span><strong>${s.min():,.2f}</strong></div>
                <div class='stat-row'><span>Max</span><strong>${s.max():,.2f}</strong></div>
                <div class='stat-row'><span>Total</span><strong>${s.sum():,.0f}</strong></div>
            </div>""", unsafe_allow_html=True)
        with stat_cols[3]:
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-box-title'>Percentiles</div>
                <div class='stat-row'><span>25th</span><strong>${s.quantile(0.25):,.2f}</strong></div>
                <div class='stat-row'><span>75th</span><strong>${s.quantile(0.75):,.2f}</strong></div>
                <div class='stat-row'><span>90th</span><strong>${s.quantile(0.90):,.2f}</strong></div>
            </div>""", unsafe_allow_html=True)

        # Sales distribution histogram
        fig_hist = px.histogram(
            fdf, x="Sales", nbins=60,
            color_discrete_sequence=["#2563EB"],
            labels={"Sales": "Order Value (USD)"},
        )
        fig_hist.update_layout(**chart_layout(
            height=240,
            xaxis=dict(tickprefix="$", tickformat=","),
            yaxis=dict(title="Count"),
        ))
        st.plotly_chart(fig_hist, use_container_width=True, key="ov_hist")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Revenue by Category")
        d = fdf.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=True)
        fig = px.bar(d, x="Sales", y="Category", orientation="h",
                     color="Category", color_discrete_map=CAT_COLORS, text_auto=".2s")
        fig.update_layout(**chart_layout(height=280, showlegend=False,
                          xaxis=dict(tickprefix="$", tickformat=",")))
        st.plotly_chart(fig, use_container_width=True, key="ov_cat")

    with col2:
        st.markdown("#### Revenue by Region")
        d = fdf.groupby("Region")["Sales"].sum().reset_index()
        fig = px.pie(d, names="Region", values="Sales",
                     color="Region", color_discrete_map=REG_COLORS, hole=0.48)
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          textfont=dict(color="black"))
        fig.update_layout(**chart_layout(height=280))
        st.plotly_chart(fig, use_container_width=True, key="ov_reg")

    # ── Top 10 Products bar chart (NEW) ──────────────────────────────────────
    st.markdown("#### 🥇 Top 10 Products by Revenue")
    top10 = (fdf.groupby(["Product Name", "Category"])["Sales"]
             .sum().reset_index()
             .sort_values("Sales", ascending=False)
             .head(10)
             .sort_values("Sales", ascending=True))
    top10["Label"] = top10["Product Name"].str[:55]
    fig = px.bar(top10, x="Sales", y="Label", orientation="h",
                 color="Category", color_discrete_map=CAT_COLORS, text_auto=".2s")
    fig.update_layout(**chart_layout(height=360,
                      xaxis=dict(tickprefix="$", tickformat=",")))
    st.plotly_chart(fig, use_container_width=True, key="ov_top10")

    st.markdown("---")
    st.markdown("#### 📋 Sample Orders")

    top_n = st.slider("Rows to show", 5, 50, 15, key="ov_rows")
    display_cols = ["Order ID", "Order Date", "Customer Name", "Segment",
                    "State", "Category", "Sub-Category", "Product Name", "Sales"]
    sample_df = fdf[display_cols].head(top_n).copy()
    st.dataframe(
        sample_df.style.format({
            "Sales": "${:,.2f}",
            "Order Date": lambda x: x.strftime("%d %b %Y"),
        }),
        use_container_width=True,
    )

    download_csv(fdf)


# =============================================================================
# PAGE 2 — TREND ANALYSIS
# =============================================================================
elif page == "📈  Trend Analysis":
    st.markdown('<div class="section-header">📈 Monthly Sales Trend Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box"><b>What to look for:</b> A consistent Q4 spike (Oct–Dec) every year signals seasonal demand — the store\'s biggest revenue window.</div>', unsafe_allow_html=True)

    monthly = fdf.groupby("Year-Month")["Sales"].sum().reset_index().sort_values("Year-Month")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Year-Month"], y=monthly["Sales"],
        mode="lines+markers",
        line=dict(color="#2563EB", width=2.5),
        marker=dict(size=6, color="#2563EB"),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.1)",
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    ))

    # Add 3-month rolling average line
    monthly["Rolling3"] = monthly["Sales"].rolling(3, min_periods=1).mean()
    fig.add_trace(go.Scatter(
        x=monthly["Year-Month"], y=monthly["Rolling3"],
        mode="lines", name="3-Month Avg",
        line=dict(color="#EF4444", width=2, dash="dot"),
        hovertemplate="3M Avg: $%{y:,.0f}<extra></extra>",
    ))

    fig.update_layout(**chart_layout(height=380,
                      xaxis=dict(title="Month", tickangle=45, showgrid=False),
                      yaxis=dict(title="Total Sales (USD)", tickprefix="$",
                                 tickformat=",", gridcolor="#E5E7EB"),
                      hovermode="x unified",
                      showlegend=True))
    st.plotly_chart(fig, use_container_width=True, key="trend_monthly")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Sales by Quarter (per Year)")
        d = fdf.groupby(["Year", "Quarter"])["Sales"].sum().reset_index()
        fig = px.bar(d, x="Quarter", y="Sales", color="Year", barmode="group",
                     color_discrete_sequence=["#93C5FD", "#2563EB", "#1E3A8A", "#172554"],
                     text_auto=".2s")
        fig.update_layout(**chart_layout(height=320,
                          yaxis=dict(tickprefix="$", tickformat=",")))
        st.plotly_chart(fig, use_container_width=True, key="trend_quarter")

    with col2:
        st.markdown("#### Year-over-Year Annual Sales")
        d = fdf.groupby("Year")["Sales"].sum().reset_index()
        d["Growth"] = d["Sales"].pct_change().mul(100).round(1)
        fig = px.bar(d, x="Year", y="Sales",
                     color="Sales",
                     color_continuous_scale=["#DBEAFE", "#2563EB", "#1E3A8A"],
                     text_auto=".2s",
                     hover_data={"Growth": ":.1f"})
        fig.update_layout(**chart_layout(height=320, coloraxis_showscale=False,
                          yaxis=dict(tickprefix="$", tickformat=",")))
        st.plotly_chart(fig, use_container_width=True, key="trend_yearly")

    # Month-over-Month comparison (NEW) ─────────────────────────────────────
    st.markdown("#### 📅 Month-by-Month Comparison Across Years")
    mo_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    d_mo = fdf.groupby(["Year","Month Name","Month Num"])["Sales"].sum().reset_index()
    d_mo = d_mo.sort_values("Month Num")
    # Set month name as ordered category
    d_mo["Month Name"] = pd.Categorical(d_mo["Month Name"], categories=mo_order, ordered=True)
    d_mo = d_mo.sort_values(["Year","Month Name"])
    fig = px.line(d_mo, x="Month Name", y="Sales", color="Year",
                  color_discrete_sequence=["#93C5FD","#2563EB","#1E3A8A","#172554"],
                  markers=True)
    fig.update_layout(**chart_layout(height=320,
                      xaxis=dict(title="Month", showgrid=False),
                      yaxis=dict(tickprefix="$", tickformat=",", gridcolor="#E5E7EB")))
    st.plotly_chart(fig, use_container_width=True, key="trend_mom")

    if len(monthly) > 0:
        peak  = monthly.loc[monthly["Sales"].idxmax()]
        trough = monthly.loc[monthly["Sales"].idxmin()]
        c1, c2 = st.columns(2)
        c1.info(f"🏆 **Peak Month:** {peak['Year-Month']}  →  **${peak['Sales']:,.0f}**")
        c2.info(f"📉 **Slowest Month:** {trough['Year-Month']}  →  **${trough['Sales']:,.0f}**")

    download_csv(fdf)


# =============================================================================
# PAGE 3 — CATEGORY ANALYSIS
# =============================================================================
elif page == "📦  Category Analysis":
    st.markdown('<div class="section-header">📦 Category & Sub-Category Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box"><b>Key insight:</b> Technology generates the highest revenue per order. Office Supplies have the most transactions but smallest individual values.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Total Sales by Category")
        d = fdf.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=True)
        fig = px.bar(d, x="Sales", y="Category", orientation="h",
                     color="Category", color_discrete_map=CAT_COLORS, text_auto=".2s")
        fig.update_layout(**chart_layout(height=280, showlegend=False,
                          xaxis=dict(tickprefix="$", tickformat=",")))
        st.plotly_chart(fig, use_container_width=True, key="cat_sales")

    with col2:
        st.markdown("#### Order Count by Category")
        d = fdf.groupby("Category").size().reset_index(name="Orders").sort_values("Orders", ascending=True)
        fig = px.bar(d, x="Orders", y="Category", orientation="h",
                     color="Category", color_discrete_map=CAT_COLORS, text_auto=True)
        fig.update_layout(**chart_layout(height=280, showlegend=False))
        st.plotly_chart(fig, use_container_width=True, key="cat_orders")

    st.markdown("#### Top 10 Sub-Categories by Revenue")
    sub = (fdf.groupby(["Sub-Category","Category"])["Sales"]
           .sum().reset_index()
           .sort_values("Sales", ascending=False)
           .head(10)
           .sort_values("Sales", ascending=True))
    fig = px.bar(sub, x="Sales", y="Sub-Category", color="Category",
                 orientation="h", color_discrete_map=CAT_COLORS, text_auto=".2s")
    fig.update_layout(**chart_layout(height=360,
                      xaxis=dict(tickprefix="$", tickformat=",")))
    st.plotly_chart(fig, use_container_width=True, key="cat_subcat")

    st.markdown("#### Category → Sub-Category Treemap")
    tree = fdf.groupby(["Category","Sub-Category"])["Sales"].sum().reset_index()
    fig = px.treemap(tree, path=[px.Constant("All Categories"), "Category", "Sub-Category"],
                     values="Sales",
                     color="Category", color_discrete_map=CAT_COLORS,
                     hover_data={"Sales": ":,.0f"})
    fig.update_traces(root_color="#F0F4F8",
                      textfont=dict(color="black"),
                      insidetextfont=dict(color="black"))
    fig.update_layout(**chart_layout(height=420))
    st.plotly_chart(fig, use_container_width=True, key="cat_treemap")

    # Sales distribution by category — box plot (NEW) ────────────────────────
    st.markdown("#### 📦 Sales Distribution per Category (Box Plot)")
    fig_box = px.box(fdf, x="Category", y="Sales",
                     color="Category", color_discrete_map=CAT_COLORS,
                     points="outliers")
    fig_box.update_layout(**chart_layout(height=340, showlegend=False,
                          yaxis=dict(tickprefix="$", tickformat=",")))
    st.plotly_chart(fig_box, use_container_width=True, key="cat_box")

    top_n_prod = st.slider("Show top N products", 5, 30, 15, key="cat_topn")
    st.markdown(f"#### Top {top_n_prod} Best-Selling Products")
    top_prods = (fdf.groupby("Product Name")["Sales"]
                 .sum().reset_index()
                 .sort_values("Sales", ascending=False)
                 .head(top_n_prod))
    top_prods["Rank"] = range(1, len(top_prods)+1)
    top_prods = top_prods[["Rank","Product Name","Sales"]]
    st.dataframe(top_prods.style.format({"Sales": "${:,.2f}"}), use_container_width=True)

    download_csv(fdf)


# =============================================================================
# PAGE 4 — CUSTOMER SEGMENTS
# =============================================================================
elif page == "👥  Customer Segments":
    st.markdown('<div class="section-header">👥 Customer Segment Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box"><b>Key insight:</b> Consumers dominate by volume (~50%), but Corporate orders carry higher average values — each segment needs a tailored strategy.</div>', unsafe_allow_html=True)

    seg_sales  = fdf.groupby("Segment")["Sales"].sum()
    seg_orders = fdf.groupby("Segment").size()
    seg_avg    = fdf.groupby("Segment")["Sales"].mean()
    seg_custs  = fdf.groupby("Segment")["Customer Name"].nunique()

    c1, c2, c3 = st.columns(3)
    for col, seg, color in zip([c1, c2, c3],
                                ["Consumer","Corporate","Home Office"],
                                ["#2563EB","#10B981","#F59E0B"]):
        if seg in seg_sales.index:
            with col:
                st.markdown(kpi(
                    seg, f"${seg_sales[seg]:,.0f}",
                    f"{seg_orders[seg]:,} orders · {seg_custs[seg]} customers · avg ${seg_avg[seg]:,.0f}",
                    color,
                ), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Revenue Share by Segment")
        d = seg_sales.reset_index()
        fig = px.pie(d, names="Segment", values="Sales",
                     color="Segment", color_discrete_map=SEG_COLORS, hole=0.5)
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          textfont=dict(color="black"))
        fig.update_layout(**chart_layout(height=340))
        st.plotly_chart(fig, use_container_width=True, key="seg_pie")

    with col2:
        st.markdown("#### Sales by Segment & Category")
        d = fdf.groupby(["Segment","Category"])["Sales"].sum().reset_index()
        fig = px.bar(d, x="Segment", y="Sales", color="Category",
                     barmode="group", color_discrete_map=CAT_COLORS, text_auto=".2s")
        fig.update_layout(**chart_layout(height=340,
                          yaxis=dict(tickprefix="$", tickformat=",")))
        st.plotly_chart(fig, use_container_width=True, key="seg_cat")

    st.markdown("#### Segment Sales Trend Over Time")
    d = fdf.groupby(["Year-Month","Segment"])["Sales"].sum().reset_index().sort_values("Year-Month")
    fig = px.line(d, x="Year-Month", y="Sales", color="Segment",
                  color_discrete_map=SEG_COLORS, markers=True)
    fig.update_layout(**chart_layout(height=340,
                      xaxis=dict(tickangle=45, showgrid=False),
                      yaxis=dict(tickprefix="$", tickformat=",", gridcolor="#E5E7EB")))
    st.plotly_chart(fig, use_container_width=True, key="seg_trend")

    st.markdown("#### Ship Mode Preference by Segment")
    d = fdf.groupby(["Segment","Ship Mode"]).size().reset_index(name="Count")
    fig = px.bar(d, x="Segment", y="Count", color="Ship Mode", barmode="stack",
                 color_discrete_map=SHIP_COLORS)
    fig.update_layout(**chart_layout(height=300))
    st.plotly_chart(fig, use_container_width=True, key="seg_ship")

    # Top customers per segment (NEW) ────────────────────────────────────────
    st.markdown("#### 🏅 Top 5 Customers per Segment")
    top_cust_cols = st.columns(3)
    for col_widget, seg in zip(top_cust_cols, ["Consumer","Corporate","Home Office"]):
        seg_df = fdf[fdf["Segment"] == seg]
        if len(seg_df) == 0:
            continue
        top5 = (seg_df.groupby("Customer Name")["Sales"]
                .sum().reset_index()
                .sort_values("Sales", ascending=False)
                .head(5))
        with col_widget:
            st.markdown(f"**{seg}**")
            st.dataframe(
                top5.rename(columns={"Customer Name":"Customer"})
                    .style.format({"Sales": "${:,.0f}"}),
                use_container_width=True, hide_index=True,
            )

    download_csv(fdf)


# =============================================================================
# PAGE 5 — GEOSPATIAL ANALYSIS
# =============================================================================
elif page == "🗺️  Geospatial Analysis":
    st.markdown('<div class="section-header">🗺️ Geospatial Sales Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box"><b>Key insight:</b> High-population coastal states (California, New York, Texas) dominate sales — urban density drives purchasing volume.</div>', unsafe_allow_html=True)

    state_data = (fdf.groupby(["State","Region"])
                  .agg(Sales=("Sales","sum"), Orders=("Sales","count"), Avg=("Sales","mean"))
                  .reset_index().sort_values("Sales", ascending=False))

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown("#### Top 15 States by Revenue")
        top15 = state_data.head(15).sort_values("Sales", ascending=True)
        fig = px.bar(top15, x="Sales", y="State", color="Region",
                     orientation="h", color_discrete_map=REG_COLORS, text_auto=".2s")
        fig.update_layout(**chart_layout(height=480,
                          xaxis=dict(tickprefix="$", tickformat=",")))
        st.plotly_chart(fig, use_container_width=True, key="geo_states")

    with col2:
        st.markdown("#### Revenue by Region")
        d = fdf.groupby("Region")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
        fig = px.funnel(d, x="Sales", y="Region", color="Region",
                        color_discrete_map=REG_COLORS)
        fig.update_layout(**chart_layout(height=480, showlegend=False))
        st.plotly_chart(fig, use_container_width=True, key="geo_regions")

    st.markdown("#### Top 10 Cities by Revenue")
    city_data = (fdf.groupby(["City","State","Region"])["Sales"]
                 .sum().reset_index().sort_values("Sales", ascending=False)
                 .head(10).sort_values("Sales", ascending=True))
    fig = px.bar(city_data, x="Sales", y="City", color="Region",
                 orientation="h", color_discrete_map=REG_COLORS,
                 text_auto=".2s", hover_data=["State"])
    fig.update_layout(**chart_layout(height=360,
                      xaxis=dict(tickprefix="$", tickformat=",")))
    st.plotly_chart(fig, use_container_width=True, key="geo_cities")

    # Orders per state bar (NEW) ──────────────────────────────────────────────
    st.markdown("#### 🗺️ Orders per State (Top 15)")
    top15_ord = state_data.sort_values("Orders", ascending=False).head(15).sort_values("Orders", ascending=True)
    fig = px.bar(top15_ord, x="Orders", y="State", color="Region",
                 orientation="h", color_discrete_map=REG_COLORS, text_auto=True)
    fig.update_layout(**chart_layout(height=420))
    st.plotly_chart(fig, use_container_width=True, key="geo_ord")

    st.markdown("#### Full State-wise Sales Table")
    state_data.index = range(1, len(state_data)+1)
    st.dataframe(
        state_data.style.format({"Sales": "${:,.0f}", "Avg": "${:,.0f}"}),
        use_container_width=True,
    )

    download_csv(fdf)


# =============================================================================
# PAGE 6 — SHIPPING ANALYSIS
# =============================================================================
elif page == "🚚  Shipping Analysis":
    st.markdown('<div class="section-header">🚚 Shipping Mode & Delivery Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box"><b>Key insight:</b> Standard Class dominates usage, but Same Day and First Class orders carry significantly higher average sales values.</div>', unsafe_allow_html=True)

    ship_rev  = fdf.groupby("Ship Mode")["Sales"].sum().reset_index()
    ship_cnt  = fdf.groupby("Ship Mode").size().reset_index(name="Orders")
    ship_avg  = fdf.groupby("Ship Mode")["Sales"].mean().reset_index()
    ship_days = fdf.groupby("Ship Mode")["Ship Days"].mean().reset_index()

    cols = st.columns(4)
    for col, (_, row) in zip(cols, ship_rev.iterrows()):
        mode   = row["Ship Mode"]
        sales  = row["Sales"]
        orders = ship_cnt[ship_cnt["Ship Mode"]==mode]["Orders"].values
        orders = orders[0] if len(orders) > 0 else 0
        avg    = ship_avg[ship_avg["Ship Mode"]==mode]["Sales"].values
        avg    = avg[0] if len(avg) > 0 else 0
        days   = ship_days[ship_days["Ship Mode"]==mode]["Ship Days"].values
        days   = days[0] if len(days) > 0 else 0
        with col:
            st.markdown(kpi(
                mode, f"${sales:,.0f}",
                f"{orders:,} orders · avg ${avg:,.0f} · {days:.1f} days",
                SHIP_COLORS.get(mode, "#2563EB"),
            ), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Orders per Ship Mode")
        fig = px.pie(ship_cnt, names="Ship Mode", values="Orders",
                     color="Ship Mode", color_discrete_map=SHIP_COLORS, hole=0.45)
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          textfont=dict(color="black"))
        fig.update_layout(**chart_layout(height=320))
        st.plotly_chart(fig, use_container_width=True, key="ship_pie")

    with col2:
        st.markdown("#### Average Sales per Ship Mode")
        fig = px.bar(ship_avg.sort_values("Sales", ascending=True),
                     x="Sales", y="Ship Mode", orientation="h",
                     color="Ship Mode", color_discrete_map=SHIP_COLORS, text_auto=".2s")
        fig.update_layout(**chart_layout(height=320, showlegend=False,
                          xaxis=dict(tickprefix="$", tickformat=",")))
        st.plotly_chart(fig, use_container_width=True, key="ship_avg")

    st.markdown("#### Average Shipping Days by Mode")
    fig = px.bar(ship_days.sort_values("Ship Days"),
                 x="Ship Days", y="Ship Mode", orientation="h",
                 color="Ship Mode", color_discrete_map=SHIP_COLORS, text_auto=".1f")
    fig.update_layout(**chart_layout(height=280, showlegend=False,
                      xaxis=dict(title="Avg Days to Ship")))
    st.plotly_chart(fig, use_container_width=True, key="ship_days_bar")

    st.markdown("#### Ship Mode Usage by Category")
    d = fdf.groupby(["Category","Ship Mode"]).size().reset_index(name="Orders")
    fig = px.bar(d, x="Category", y="Orders", color="Ship Mode",
                 barmode="group", color_discrete_map=SHIP_COLORS)
    fig.update_layout(**chart_layout(height=320))
    st.plotly_chart(fig, use_container_width=True, key="ship_cat")

    # Ship days distribution (NEW) ─────────────────────────────────────────────
    st.markdown("#### 📦 Shipping Days Distribution per Mode")
    fig_vio = px.violin(fdf, x="Ship Mode", y="Ship Days",
                        color="Ship Mode", color_discrete_map=SHIP_COLORS,
                        box=True, points="outliers")
    fig_vio.update_layout(**chart_layout(height=340, showlegend=False,
                          yaxis=dict(title="Days to Ship")))
    st.plotly_chart(fig_vio, use_container_width=True, key="ship_violin")

    download_csv(fdf)


# =============================================================================
# PAGE 7 — BUSINESS INSIGHTS
# =============================================================================
elif page == "💡  Business Insights":
    st.markdown('<div class="section-header">💡 Business Insights & Recommendations</div>', unsafe_allow_html=True)

    total_sales = fdf["Sales"].sum()

    def safe_idxmax(series):
        try:
            return series.idxmax()
        except Exception:
            return "N/A"

    top_cat     = safe_idxmax(fdf.groupby("Category")["Sales"].sum())
    peak_month  = safe_idxmax(fdf.groupby("Year-Month")["Sales"].sum())
    top_segment = safe_idxmax(fdf.groupby("Segment")["Sales"].sum())
    top_state   = safe_idxmax(fdf.groupby("State")["Sales"].sum())
    top_cust    = safe_idxmax(fdf.groupby("Customer Name")["Sales"].sum())
    top_subcats = (fdf.groupby("Sub-Category")["Sales"].sum()
                   .sort_values(ascending=False).index[:3].tolist())
    top_city    = safe_idxmax(fdf.groupby("City")["Sales"].sum())

    # ── Metrics grid ─────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Top Revenue Category",  top_cat,    "Highest total sales")
        st.metric("Peak Sales Month",       peak_month, "Best performing month")
    with c2:
        st.metric("Top Customer Segment",  top_segment, "Largest revenue share")
        st.metric("Top Performing State",  top_state,   "Highest state revenue")
    with c3:
        st.metric("Top Customer",  top_cust[:28] if top_cust!="N/A" else "N/A", "By lifetime spend")
        st.metric("Total Revenue", f"${total_sales:,.0f}", f"{len(fdf):,} orders")

    st.markdown("---")

    # ── Quick-facts bar (NEW) ─────────────────────────────────────────────────
    fact_cols = st.columns(4)
    with fact_cols[0]:
        st.markdown(kpi("Top City",       top_city,                    "Highest city revenue",   "#8B5CF6"), unsafe_allow_html=True)
    with fact_cols[1]:
        st.markdown(kpi("Top Sub-Cat #1", top_subcats[0] if top_subcats else "N/A", "Best sub-category", "#10B981"), unsafe_allow_html=True)
    with fact_cols[2]:
        st.markdown(kpi("Avg Ship Days",  f"{fdf['Ship Days'].mean():.1f}d", "Across all orders",  "#F59E0B"), unsafe_allow_html=True)
    with fact_cols[3]:
        monthly_avg = fdf.groupby("Year-Month")["Sales"].sum().mean()
        st.markdown(kpi("Monthly Avg",    f"${monthly_avg:,.0f}",       "Average monthly revenue","#EF4444"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Top 3 Strategic Recommendations")

    st.markdown("""
    <div class="rec-card">
        <div class="rec-title">🚀 #1 — Launch a Dedicated Q4 Campaign (September prep, 12-week runway)</div>
        <div class="rec-body">
        Sales spike 30–80% every Oct–Dec across all years in the dataset. Pre-position stock in
        September, run email campaigns in October, and offer Technology bundles in November.
        A structured Q4 campaign could add <b>10–15% to annual revenue</b> with minimal extra cost.
        </div>
    </div>
    <div class="rec-card">
        <div class="rec-title">💻 #2 — Prioritise Technology Up-Sells in Every Transaction</div>
        <div class="rec-body">
        Technology is the top revenue category with the highest average order value. Train staff to
        recommend Accessories alongside Phones and Machines. Bundle pricing (Phone + Accessories)
        increases order value while improving customer satisfaction. A <b>5% attach-rate improvement
        could add $25,000+ annually</b> based on current volume.
        </div>
    </div>
    <div class="rec-card">
        <div class="rec-title">🤝 #3 — Build a Corporate Account Programme</div>
        <div class="rec-body">
        Corporate customers are fewer in number but higher in average value. Assign dedicated account
        managers to the top 30 corporate clients, offer volume-pricing tiers, and hold quarterly
        business reviews. Improving Corporate renewal rates by 20% could
        <b>add $60,000+ to annual revenue</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Summary Charts")

    col1, col2 = st.columns(2)
    with col1:
        d = fdf.groupby(["Category","Segment"])["Sales"].sum().reset_index()
        fig = px.sunburst(d, path=[px.Constant("All"), "Category", "Segment"],
                          values="Sales",
                          color="Category", color_discrete_map=CAT_COLORS)
        fig.update_traces(insidetextorientation="radial",
                          textfont=dict(color="black"),
                          insidetextfont=dict(color="black"),
                          root_color="#F0F4F8")
        fig.update_layout(**chart_layout(height=400, title="Category & Segment Revenue"))
        st.plotly_chart(fig, use_container_width=True, key="ins_sun")

    with col2:
        heat = fdf.groupby(["Year","Month Name"])["Sales"].sum().reset_index()
        mo   = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        pivot = heat.pivot(index="Year", columns="Month Name", values="Sales")
        pivot = pivot.reindex(columns=[m for m in mo if m in pivot.columns])
        fig = px.imshow(pivot, color_continuous_scale=["#DBEAFE","#2563EB","#1E3A8A"],
                        aspect="auto", text_auto=".2s")
        fig.update_layout(**chart_layout(height=400, title="Sales Heatmap (Year × Month)"))
        st.plotly_chart(fig, use_container_width=True, key="ins_heat")

    st.markdown("#### Top 10 Customers by Revenue")
    top_custs = (fdf.groupby("Customer Name")["Sales"]
                 .sum().reset_index()
                 .sort_values("Sales", ascending=True)
                 .tail(10))
    fig = px.bar(top_custs, x="Sales", y="Customer Name", orientation="h",
                 color="Sales", color_continuous_scale=["#DBEAFE","#2563EB","#1E3A8A"],
                 text_auto=".2s")
    fig.update_layout(**chart_layout(height=360, coloraxis_showscale=False,
                      xaxis=dict(tickprefix="$", tickformat=",")))
    st.plotly_chart(fig, use_container_width=True, key="ins_custs")

    download_csv(fdf)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#6B7280; font-size:12px; padding:20px;'>"
    "Built with Streamlit &amp; Plotly · Superstore Sales Dashboard · 2024 · "
    "Vivek · Yash · Param · Harishta"
    "</div>",
    unsafe_allow_html=True,
)
