#  SUPERSTORE SALES — INTERACTIVE STREAMLIT DASHBOARD
#  Course Project | Data Analytics
#  Author : vivek 
#  HOW TO RUN:
#      pip install streamlit plotly pandas
#      streamlit run app.py
#
#  This opens a browser at http://localhost:8501
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

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

/* ─────────────────────────────
   SIDEBAR
───────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0F2057 0%, #1E3A8A 50%, #1D4ED8 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.18);
    min-width: 260px !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding-top: 1.5rem;
}

/* Force ALL sidebar text white */
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
}

/* Radio button pills */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    cursor: pointer;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: 0.2s ease;
    display: block;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.18) !important;
    border-color: rgba(255,255,255,0.35) !important;
    transform: translateX(3px);
}

/* Selected radio */
[data-testid="stSidebar"] .stRadio label[data-checked="true"],
[data-testid="stSidebar"] .stRadio input:checked + div {
    background: rgba(255,255,255,0.22) !important;
    border-color: rgba(255,255,255,0.5) !important;
}

/* MultiSelect chips */
[data-testid="stSidebar"] .stMultiSelect span,
[data-testid="stSidebar"] .stMultiSelect div {
    color: white !important;
}

[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(255,255,255,0.2) !important;
}

/* Divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
}

/* Sidebar logo box */
.sidebar-logo {
    background: rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 18px 14px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.2);
    text-align: center;
}

/* ─────────────────────────────
   PAGE BANNER
───────────────────────────── */
.page-banner {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 60%, #3B82F6 100%);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 32px rgba(37,99,235,0.25);
    position: relative;
    overflow: hidden;
}

.page-banner::before, .page-banner::after {
    content: '';
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}

.page-banner::before { top: -40px; right: -40px; width: 180px; height: 180px; }
.page-banner::after  { bottom: -60px; right: 80px; width: 240px; height: 240px; }

.banner-title { font-size: 26px; font-weight: 800; color: white; margin-bottom: 4px; }
.banner-sub   { font-size: 13px; color: rgba(255,255,255,0.75); }
.banner-badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    padding: 6px 16px;
    font-size: 12px;
    color: white;
    font-weight: 600;
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
    transition: 0.2s;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.10);
}

.kpi-label { font-size: 10px; color: #9CA3AF; font-weight: 700; text-transform: uppercase; }
.kpi-value { font-size: 24px; font-weight: 800; color: #111827; }
.kpi-sub   { font-size: 11px; color: #9CA3AF; }

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
    color: black;
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
   TABLE & METRICS
───────────────────────────── */
[data-testid="stDataFrame"],
[data-testid="stMetric"] {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

/* ─────────────────────────────
   HEADINGS
───────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: black !important;
}

/* Section header */
.section-header {
    font-size: 22px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 18px;
}

/* ─────────────────────────────
   HIDE STREAMLIT UI
───────────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# BACKEND — DATA LOADING & CLEANING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, "train.csv"))

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True)

    df["Postal Code"] = df["Postal Code"].fillna(0).astype(int)

    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"]       = df["Order Date"].dt.year
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Quarter"]    = "Q" + df["Order Date"].dt.quarter.astype(str)
    df["Ship Days"]  = (df["Ship Date"] - df["Order Date"]).dt.days

    return df

df = load_data()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Navigation + Filters
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:32px;">🛒</div>
        <div style="font-size:17px; font-weight:800; margin-top:6px; color:white;">Superstore EDA</div>
        <div style="font-size:11px; opacity:0.75; margin-top:3px; color:white;">Data Analytics Project</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio("Navigate to", [
        "🏠  Overview",
        "📈  Trend Analysis",
        "📦  Category Analysis",
        "👥  Customer Segments",
        "🗺️  Geospatial Analysis",
        "🚚  Shipping Analysis",
        "💡  Business Insights"
    ])

    st.markdown("---")
    st.markdown("### 🔧 Filters")

    years = sorted(df["Year"].unique())
    selected_years = st.multiselect("Year", years, default=years)

    regions = sorted(df["Region"].unique())
    selected_regions = st.multiselect("Region", regions, default=regions)

    categories = sorted(df["Category"].unique())
    selected_cats = st.multiselect("Category", categories, default=categories)

    segments = sorted(df["Segment"].unique())
    selected_segs = st.multiselect("Segment", segments, default=segments)

    st.markdown("---")
    st.markdown("**Author:** Vivek Pant, Yash, Param, Harishta")
    st.markdown(f"**Dataset:** {len(df):,} real orders")
    st.markdown("**Period:** 2014 – 2017")

# Apply filters
fdf = df[
    df["Year"].isin(selected_years) &
    df["Region"].isin(selected_regions) &
    df["Category"].isin(selected_cats) &
    df["Segment"].isin(selected_segs)
]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def kpi(label, value, sub="", color="#2563EB"):
    return f"""<div class="kpi-card" style="border-left-color:{color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

# ── All chart labels forced black ──────────────────────────────────────────
BLACK_FONT = dict(color="black")
AXIS_STYLE = dict(tickfont=BLACK_FONT, title_font=BLACK_FONT, color="black")

CHART_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=0, r=0, t=30, b=0),
    font=dict(family="Inter, Segoe UI, sans-serif", color="black"),
    legend=dict(font=BLACK_FONT, title_font=BLACK_FONT),
    title_font=BLACK_FONT,
)

CAT_COLORS = {"Furniture": "#10B981", "Office Supplies": "#F59E0B", "Technology": "#2563EB"}
REG_COLORS = {"West": "#2563EB", "East": "#10B981", "Central": "#F59E0B", "South": "#EF4444"}
SEG_COLORS = {"Consumer": "#2563EB", "Corporate": "#10B981", "Home Office": "#F59E0B"}


# =============================================================================
# PAGE 1 — OVERVIEW
# =============================================================================
if page == "🏠  Overview":
    st.markdown('<div class="section-header">🏠 Project Overview Dashboard</div>', unsafe_allow_html=True)

    total_sales  = fdf["Sales"].sum()
    total_orders = len(fdf)
    avg_order    = fdf["Sales"].mean()
    unique_custs = fdf["Customer Name"].nunique()
    unique_prods = fdf["Product Name"].nunique()
    top_state    = fdf.groupby("State")["Sales"].sum().idxmax()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi("Total Revenue",    f"${total_sales:,.0f}", "All filtered orders",     "#2563EB"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Orders",     f"{total_orders:,}",    "Transactions",             "#10B981"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Avg Order Value",  f"${avg_order:,.0f}",   "Per transaction",          "#F59E0B"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Unique Customers", f"{unique_custs:,}",    "Individual buyers",        "#8B5CF6"), unsafe_allow_html=True)
    with c5: st.markdown(kpi("Products Sold",    f"{unique_prods:,}",    f"Top state: {top_state}",  "#EF4444"), unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Revenue by Category")
        d = fdf.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=True)
        fig = px.bar(d, x="Sales", y="Category", orientation="h",
                     color="Category", color_discrete_map=CAT_COLORS, text_auto=".2s")
        fig.update_layout(**CHART_LAYOUT, height=280, showlegend=False,
                          xaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Revenue by Region")
        d = fdf.groupby("Region")["Sales"].sum().reset_index()
        fig = px.pie(d, names="Region", values="Sales",
                     color="Region", color_discrete_map=REG_COLORS, hole=0.48)
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          textfont=dict(color="black"))
        fig.update_layout(**CHART_LAYOUT, height=280)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Sample Orders (first 15 rows)")
    display_cols = ["Order ID","Order Date","Customer Name","Segment","State",
                    "Category","Sub-Category","Product Name","Sales"]
    st.dataframe(
        fdf[display_cols].head(15).style.format({"Sales": "${:,.2f}", "Order Date": lambda x: x.strftime("%d %b %Y")}),
        use_container_width=True
    )


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
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(**CHART_LAYOUT, height=380,
                      xaxis=dict(**AXIS_STYLE, title="Month", tickangle=45, showgrid=False),
                      yaxis=dict(**AXIS_STYLE, title="Total Sales (USD)", tickprefix="$",
                                 tickformat=",", gridcolor="#E5E7EB"),
                      hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Sales by Quarter (per Year)")
        d = fdf.groupby(["Year","Quarter"])["Sales"].sum().reset_index()
        fig = px.bar(d, x="Quarter", y="Sales", color="Year", barmode="group",
                     color_discrete_sequence=["#93C5FD","#2563EB","#1E3A8A","#172554"],
                     text_auto=".2s")
        fig.update_layout(**CHART_LAYOUT, height=320,
                          xaxis=AXIS_STYLE,
                          yaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Year-over-Year Annual Sales")
        d = fdf.groupby("Year")["Sales"].sum().reset_index()
        fig = px.bar(d, x="Year", y="Sales", color="Sales",
                     color_continuous_scale=["#DBEAFE","#2563EB","#1E3A8A"],
                     text_auto=".2s")
        fig.update_layout(**CHART_LAYOUT, height=320, coloraxis_showscale=False,
                          xaxis=AXIS_STYLE,
                          yaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","))
        st.plotly_chart(fig, use_container_width=True)

    peak = monthly.loc[monthly["Sales"].idxmax()]
    st.info(f"🏆 **Peak Month:** {peak['Year-Month']}  →  **${peak['Sales']:,.0f}** in sales")


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
        fig.update_layout(**CHART_LAYOUT, height=280, showlegend=False,
                          xaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","),
                          yaxis=AXIS_STYLE)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Order Count by Category")
        d = fdf.groupby("Category").size().reset_index(name="Orders").sort_values("Orders", ascending=True)
        fig = px.bar(d, x="Orders", y="Category", orientation="h",
                     color="Category", color_discrete_map=CAT_COLORS, text_auto=True)
        fig.update_layout(**CHART_LAYOUT, height=280, showlegend=False,
                          xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Top 10 Sub-Categories by Revenue")
    sub = (fdf.groupby(["Sub-Category","Category"])["Sales"]
           .sum().reset_index()
           .sort_values("Sales", ascending=False)
           .head(10)
           .sort_values("Sales", ascending=True))
    fig = px.bar(sub, x="Sales", y="Sub-Category", color="Category",
                 orientation="h", color_discrete_map=CAT_COLORS, text_auto=".2s")
    fig.update_layout(**CHART_LAYOUT, height=360,
                      xaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","),
                      yaxis=AXIS_STYLE)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Category → Sub-Category Treemap")
    tree = fdf.groupby(["Category","Sub-Category"])["Sales"].sum().reset_index()
    fig = px.treemap(tree, path=["Category","Sub-Category"], values="Sales",
                     color="Category", color_discrete_map=CAT_COLORS,
                     hover_data={"Sales":":,.0f"})
    fig.update_layout(**CHART_LAYOUT, height=420)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Top 15 Best-Selling Products")
    top_prods = (fdf.groupby("Product Name")["Sales"]
                 .sum().reset_index()
                 .sort_values("Sales", ascending=False)
                 .head(15))
    top_prods["Product Name"] = top_prods["Product Name"].str[:55]
    st.dataframe(top_prods.style.format({"Sales":"${:,.2f}"}), use_container_width=True)


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
    for col, seg, color in zip([c1,c2,c3], ["Consumer","Corporate","Home Office"],
                                ["#2563EB","#10B981","#F59E0B"]):
        with col:
            st.markdown(kpi(
                seg,
                f"${seg_sales[seg]:,.0f}",
                f"{seg_orders[seg]:,} orders · {seg_custs[seg]} customers · avg ${seg_avg[seg]:,.0f}",
                color
            ), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Revenue Share by Segment")
        d = seg_sales.reset_index()
        fig = px.pie(d, names="Segment", values="Sales",
                     color="Segment", color_discrete_map=SEG_COLORS, hole=0.5)
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          textfont=dict(color="black"))
        fig.update_layout(**CHART_LAYOUT, height=340)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Sales by Segment & Category")
        d = fdf.groupby(["Segment","Category"])["Sales"].sum().reset_index()
        fig = px.bar(d, x="Segment", y="Sales", color="Category",
                     barmode="group", color_discrete_map=CAT_COLORS, text_auto=".2s")
        fig.update_layout(**CHART_LAYOUT, height=340,
                          xaxis=AXIS_STYLE,
                          yaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Segment Sales Trend Over Time")
    d = fdf.groupby(["Year-Month","Segment"])["Sales"].sum().reset_index().sort_values("Year-Month")
    fig = px.line(d, x="Year-Month", y="Sales", color="Segment",
                  color_discrete_map=SEG_COLORS, markers=True)
    fig.update_layout(**CHART_LAYOUT, height=340,
                      xaxis=dict(**AXIS_STYLE, tickangle=45, showgrid=False),
                      yaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=",", gridcolor="#E5E7EB"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Ship Mode Preference by Segment")
    d = fdf.groupby(["Segment","Ship Mode"]).size().reset_index(name="Count")
    fig = px.bar(d, x="Segment", y="Count", color="Ship Mode", barmode="stack",
                 color_discrete_sequence=["#1E3A8A","#2563EB","#60A5FA","#BFDBFE"])
    fig.update_layout(**CHART_LAYOUT, height=300,
                      xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# PAGE 5 — GEOSPATIAL ANALYSIS
# =============================================================================
elif page == "🗺️  Geospatial Analysis":
    st.markdown('<div class="section-header">🗺️ Geospatial Sales Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box"><b>Key insight:</b> High-population coastal states (California, New York, Texas) dominate sales — urban density drives purchasing volume.</div>', unsafe_allow_html=True)

    state_data = (fdf.groupby(["State","Region"])
                  .agg(Sales=("Sales","sum"), Orders=("Sales","count"), Avg=("Sales","mean"))
                  .reset_index().sort_values("Sales", ascending=False))

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### Top 15 States by Revenue")
        top15 = state_data.head(15).sort_values("Sales", ascending=True)
        fig = px.bar(top15, x="Sales", y="State", color="Region",
                     orientation="h", color_discrete_map=REG_COLORS, text_auto=".2s")
        fig.update_layout(**CHART_LAYOUT, height=480,
                          xaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","),
                          yaxis=AXIS_STYLE)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Revenue by Region")
        d = fdf.groupby("Region")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
        fig = px.funnel(d, x="Sales", y="Region", color="Region",
                        color_discrete_map=REG_COLORS)
        fig.update_layout(**CHART_LAYOUT, height=480, showlegend=False,
                          xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Top 10 Cities by Revenue")
    city_data = (fdf.groupby(["City","State","Region"])["Sales"]
                 .sum().reset_index().sort_values("Sales", ascending=False).head(10)
                 .sort_values("Sales", ascending=True))
    fig = px.bar(city_data, x="Sales", y="City", color="Region",
                 orientation="h", color_discrete_map=REG_COLORS, text_auto=".2s",
                 hover_data=["State"])
    fig.update_layout(**CHART_LAYOUT, height=360,
                      xaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","),
                      yaxis=AXIS_STYLE)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Full State-wise Sales Table")
    state_data.index = range(1, len(state_data)+1)
    st.dataframe(
        state_data.style.format({"Sales":"${:,.0f}", "Avg":"${:,.0f}"}),
        use_container_width=True
    )


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

    SHIP_COLORS = {
        "Standard Class": "#2563EB",
        "Second Class":   "#10B981",
        "First Class":    "#F59E0B",
        "Same Day":       "#EF4444"
    }

    cols = st.columns(4)
    for col, (_, row) in zip(cols, ship_rev.iterrows()):
        mode   = row["Ship Mode"]
        sales  = row["Sales"]
        orders = ship_cnt[ship_cnt["Ship Mode"]==mode]["Orders"].values[0]
        avg    = ship_avg[ship_avg["Ship Mode"]==mode]["Sales"].values[0]
        days   = ship_days[ship_days["Ship Mode"]==mode]["Ship Days"].values[0]
        with col:
            st.markdown(kpi(
                mode,
                f"${sales:,.0f}",
                f"{orders:,} orders · avg ${avg:,.0f} · {days:.1f} days",
                SHIP_COLORS.get(mode, "#2563EB")
            ), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Orders per Ship Mode")
        fig = px.pie(ship_cnt, names="Ship Mode", values="Orders",
                     color="Ship Mode", color_discrete_map=SHIP_COLORS, hole=0.45)
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          textfont=dict(color="black"))
        fig.update_layout(**CHART_LAYOUT, height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Average Sales per Ship Mode")
        fig = px.bar(ship_avg.sort_values("Sales", ascending=True),
                     x="Sales", y="Ship Mode", orientation="h",
                     color="Ship Mode", color_discrete_map=SHIP_COLORS, text_auto=".2s")
        fig.update_layout(**CHART_LAYOUT, height=320, showlegend=False,
                          xaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","),
                          yaxis=AXIS_STYLE)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Average Shipping Days by Mode")
    fig = px.bar(ship_days.sort_values("Ship Days"),
                 x="Ship Days", y="Ship Mode", orientation="h",
                 color="Ship Mode", color_discrete_map=SHIP_COLORS, text_auto=".1f")
    fig.update_layout(**CHART_LAYOUT, height=280, showlegend=False,
                      xaxis=dict(**AXIS_STYLE, title="Avg Days to Ship"),
                      yaxis=AXIS_STYLE)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Ship Mode Usage by Category")
    d = fdf.groupby(["Category","Ship Mode"]).size().reset_index(name="Orders")
    fig = px.bar(d, x="Category", y="Orders", color="Ship Mode",
                 barmode="group", color_discrete_map=SHIP_COLORS)
    fig.update_layout(**CHART_LAYOUT, height=320,
                      xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# PAGE 7 — BUSINESS INSIGHTS
# =============================================================================
elif page == "💡  Business Insights":
    st.markdown('<div class="section-header">💡 Business Insights & Recommendations</div>', unsafe_allow_html=True)

    total_sales  = fdf["Sales"].sum()
    top_cat      = fdf.groupby("Category")["Sales"].sum().idxmax()
    peak_month   = fdf.groupby("Year-Month")["Sales"].sum().idxmax()
    top_segment  = fdf.groupby("Segment")["Sales"].sum().idxmax()
    top_state    = fdf.groupby("State")["Sales"].sum().idxmax()
    top_cust     = fdf.groupby("Customer Name")["Sales"].sum().idxmax()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Top Revenue Category", top_cat,     "Highest total sales")
        st.metric("Peak Sales Month",     peak_month,  "Best performing month")
    with c2:
        st.metric("Top Customer Segment", top_segment, "Largest revenue share")
        st.metric("Top Performing State", top_state,   "Highest state revenue")
    with c3:
        st.metric("Top Customer",         top_cust[:25], "By lifetime spend")
        st.metric("Total Revenue",        f"${total_sales:,.0f}", f"{len(fdf):,} orders")

    st.markdown("---")
    st.markdown("### 🎯 Top 3 Recommendations")

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
        Corporate customers are fewer in number but higher in value. Assign dedicated account managers
        to the top 30 corporate clients, offer volume-pricing tiers, and hold quarterly business reviews.
        Improving Corporate renewal rates by 20% could <b>add $60,000+ to annual revenue</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Summary Charts")

    col1, col2 = st.columns(2)
    with col1:
        d = fdf.groupby(["Category","Segment"])["Sales"].sum().reset_index()
        fig = px.sunburst(d, path=["Category","Segment"], values="Sales",
                          color="Category", color_discrete_map=CAT_COLORS)
        fig.update_layout(**CHART_LAYOUT, height=400, title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        heat = fdf.groupby(["Year","Month Name"])["Sales"].sum().reset_index()
        mo   = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        pivot = heat.pivot(index="Year", columns="Month Name", values="Sales")
        pivot = pivot.reindex(columns=[m for m in mo if m in pivot.columns])
        fig = px.imshow(pivot, color_continuous_scale=["#DBEAFE","#2563EB","#1E3A8A"],
                        aspect="auto", text_auto=".2s")
        fig.update_layout(**CHART_LAYOUT, height=400, title="",
                          xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Top 10 Customers by Revenue")
    top_custs = (fdf.groupby("Customer Name")["Sales"]
                 .sum().reset_index()
                 .sort_values("Sales", ascending=True)
                 .tail(10))
    fig = px.bar(top_custs, x="Sales", y="Customer Name", orientation="h",
                 color="Sales", color_continuous_scale=["#DBEAFE","#2563EB","#1E3A8A"],
                 text_auto=".2s")
    fig.update_layout(**CHART_LAYOUT, height=360, coloraxis_showscale=False,
                      xaxis=dict(**AXIS_STYLE, tickprefix="$", tickformat=","),
                      yaxis=AXIS_STYLE)
    st.plotly_chart(fig, use_container_width=True)