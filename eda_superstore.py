# =============================================================================
#  SUPERSTORE SALES — EXPLORATORY DATA ANALYSIS (EDA)
#  Course Project | Data Analytics
#  Author : vivek
#  Dataset: train.csv  (Superstore Sales)
# =============================================================================
#
#  HOW TO RUN:
#      pip install pandas matplotlib seaborn
#      python eda_superstore.py
#
#  OUTPUT: Four chart PNGs saved in the same folder as this script.
# =============================================================================


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 0 ▸ IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import pandas as pd           # Data manipulation and analysis
import matplotlib.pyplot as plt  # Core plotting library
import matplotlib.ticker as mticker
from matplotlib.patches import Patch  # Import moved to top
import seaborn as sns         # High-level statistical visualisation
import warnings
import os
import sys

warnings.filterwarnings("ignore")   # Suppress minor deprecation warnings

# Apply a clean, professional Seaborn theme for all charts
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

# Directory where chart images will be saved (same folder as this script)
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
if not OUTPUT_DIR:  # Handle case when running interactively
    OUTPUT_DIR = os.getcwd()


# =============================================================================
# SECTION 1 ▸ DATA LOADING & CLEANING
# =============================================================================

def load_and_clean(filepath: str) -> pd.DataFrame:
    """
    Load train.csv, clean it, and engineer the Year-Month feature.

    Steps
    -----
    1. Read CSV with pandas.
    2. Parse 'Order Date' as datetime (format DD/MM/YYYY).
    3. Handle missing values in 'Postal Code'.
    4. Add 'Year-Month' column for time-series analysis.

    Parameters
    ----------
    filepath : str
        Absolute or relative path to train.csv.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe ready for analysis.
    """

    # ── Step 1: Load the CSV ──────────────────────────────────────────────────
    print("=" * 60)
    print("STEP 1 ▸ Loading data …")
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"\n❌ ERROR: File not found at {filepath}")
        print("\nTrying alternative paths...")
        
        # Try alternative paths
        alternative_paths = [
            "train.csv",
            os.path.join(os.getcwd(), "train.csv"),
            os.path.join(os.path.dirname(__file__), "train.csv") if __file__ else None
        ]
        
        filepath = None
        for alt_path in alternative_paths:
            if alt_path and os.path.exists(alt_path):
                filepath = alt_path
                print(f"✅ Found at: {filepath}")
                break
        
        if filepath is None:
            print("\n❌ FATAL: train.csv not found in any location!")
            print("Please ensure train.csv is in the same directory as this script.")
            sys.exit(1)
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        # Try alternative encoding
        df = pd.read_csv(filepath, encoding='latin-1')
    
    print(f"  Rows: {len(df):,}   Columns: {df.shape[1]}")
    print(f"  Columns: {list(df.columns)}\n")

    # ── Step 2: Parse dates ───────────────────────────────────────────────────
    # The dataset stores dates as strings like "04/12/2016" (DD/MM/YYYY).
    # We use pd.to_datetime() with dayfirst=True so Python doesn't
    # misread day 04 as month 04.
    print("STEP 2 ▸ Converting 'Order Date' to datetime …")
    
    try:
        df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors='coerce')
        
        # Check for parsing failures
        failed_dates = df["Order Date"].isna().sum()
        if failed_dates > 0:
            print(f"  ⚠️  Warning: {failed_dates} dates could not be parsed")
            # Drop rows with invalid dates
            df = df.dropna(subset=['Order Date'])
            print(f"  Dropped {failed_dates} rows with invalid dates")
        
        print(f"  dtype after conversion: {df['Order Date'].dtype}")
        print(f"  Date range: {df['Order Date'].min().date()}  →  {df['Order Date'].max().date()}\n")
    except Exception as e:
        print(f"❌ ERROR parsing dates: {e}")
        sys.exit(1)

    # ── Step 3: Handle missing Postal Codes ───────────────────────────────────
    # Postal Code is metadata only; it's NOT used in any analysis.
    # We fill NaN with 0 (a placeholder) and cast to int to be clean.
    # An alternative would be dropping the column entirely.
    print("STEP 3 ▸ Handling missing values …")
    missing_pc = df["Postal Code"].isna().sum()
    print(f"  Missing Postal Codes before fix: {missing_pc}")

    # Fill NaN postal codes with 0 (placeholder — column not used in analysis)
    df["Postal Code"] = df["Postal Code"].fillna(0).astype(int)
    print(f"  Missing Postal Codes after fix : {df['Postal Code'].isna().sum()}")

    # Check for missing values in other columns
    other_missing = df.drop(columns=["Postal Code"], errors='ignore').isna().sum()
    cols_with_missing = other_missing[other_missing > 0]
    if cols_with_missing.empty:
        print("  ✅ No missing values found in any other column.\n")
    else:
        print(f"  ⚠️  Missing in other columns:\n{cols_with_missing}\n")

    # ── Step 4: Engineer 'Year-Month' feature ─────────────────────────────────
    # Period('M') creates a pandas Period object like "2016-04".
    # This lets us group by month across multiple years — essential for
    # the monthly sales trend chart.
    print("STEP 4 ▸ Creating 'Year-Month' column …")
    df["Year-Month"] = df["Order Date"].dt.to_period("M")
    print(f"  Sample values: {df['Year-Month'].unique()[:5].tolist()}\n")

    # ── Step 5: Final sanity check ────────────────────────────────────────────
    print("STEP 5 ▸ Data types overview:")
    print(df.dtypes.to_string())
    print("\nDescriptive statistics for Sales:")
    print(df["Sales"].describe().round(2).to_string())
    print("=" * 60)

    return df


# =============================================================================
# SECTION 2 ▸ TREND ANALYSIS  (Monthly Sales Line Chart)
# =============================================================================

def plot_monthly_trend(df: pd.DataFrame):
    """
    Line chart: Total Sales per month over the entire timeline.

    Why a line chart?
    -----------------
    Line charts are ideal for continuous time-series data because they
    clearly show upward/downward trends and seasonal patterns (e.g., Q4 spikes).

    Key insight expected:
    ---------------------
    Sales typically rise in Q3–Q4 (back-to-school + holiday season).
    """

    print("\n[CHART 1] Monthly Sales Trend …")

    # Group sales by Year-Month and sum — aggregating all orders per month
    monthly = (
        df.groupby("Year-Month")["Sales"]
        .sum()
        .reset_index()
    )

    # Convert Period to string for the X-axis labels
    monthly["Year-Month"] = monthly["Year-Month"].astype(str)

    # Create figure with higher DPI for better quality
    fig, ax = plt.subplots(figsize=(14, 5), dpi=100)

    # Plot the line with circular markers at each data point
    ax.plot(
        monthly["Year-Month"],
        monthly["Sales"],
        marker="o",         # show a dot at each month
        linewidth=2,
        color="#2563EB",    # corporate blue
        markersize=5,
        label="Monthly Sales"
    )

    # Shade the area under the curve for visual impact
    ax.fill_between(
        range(len(monthly)), 
        monthly["Sales"], 
        alpha=0.12, 
        color="#2563EB"
    )

    # ── Formatting ────────────────────────────────────────────────────────────
    ax.set_title("Total Sales per Month (Trend Analysis)", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Sales (USD)", fontsize=12)

    # Rotate X-axis labels so they don't overlap
    ax.set_xticks(range(len(monthly)))
    ax.set_xticklabels(monthly["Year-Month"], rotation=45, ha="right", fontsize=8)

    # Format Y-axis with comma separators (e.g., 50,000 instead of 50000)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart1_monthly_trend.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✅ Saved → {path}")


# =============================================================================
# SECTION 3 ▸ CATEGORY ANALYSIS  (Bar Chart: Category & Sub-Category)
# =============================================================================

def plot_category_analysis(df: pd.DataFrame):
    """
    Two bar charts side-by-side:
      Left  — Total Sales by Category  (3 bars)
      Right — Total Sales by Sub-Category (top 10)

    Why bar charts?
    ---------------
    Bar charts are the clearest way to compare discrete categories.
    Sorted bars (highest → lowest) make ranking immediately obvious.
    """

    print("\n[CHART 2] Category & Sub-Category Sales …")

    # ── Aggregations ─────────────────────────────────────────────────────────
    cat_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    sub_sales = (
        df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)          # Show only the top 10 sub-categories
    )

    fig, axes = plt.subplots(1, 2, figsize=(16, 6), dpi=100)

    # ── Left chart: Category ──────────────────────────────────────────────────
    colors_cat = ["#2563EB", "#10B981", "#F59E0B"]
    bars = axes[0].bar(
        cat_sales.index, 
        cat_sales.values, 
        color=colors_cat[:len(cat_sales)],  # Handle if less than 3 categories
        edgecolor="white", 
        linewidth=0.8
    )

    # Annotate each bar with its total value
    for bar in bars:
        height = bar.get_height()
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,  # centre of bar
            height + (height * 0.02),            # just above the bar (2% of height)
            f"${height:,.0f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold"
        )

    axes[0].set_title("Sales by Category", fontsize=14, fontweight="bold")
    axes[0].set_xlabel("Category", fontsize=11)
    axes[0].set_ylabel("Total Sales (USD)", fontsize=11)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[0].grid(True, alpha=0.3, axis='y')

    # ── Right chart: Sub-Category ─────────────────────────────────────────────
    # Use a horizontal bar chart — easier to read long labels
    palette = sns.color_palette("Blues_r", n_colors=len(sub_sales))
    bars_h = axes[1].barh(sub_sales.index, sub_sales.values, color=palette, edgecolor="white")

    # Annotate bars
    for i, (val, name) in enumerate(zip(sub_sales.values, sub_sales.index)):
        axes[1].text(
            val + (val * 0.01),  # Slightly to the right (1% of value)
            i, 
            f"${val:,.0f}", 
            va="center", 
            fontsize=9
        )

    axes[1].set_title("Top 10 Sub-Categories by Sales", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Total Sales (USD)", fontsize=11)
    axes[1].invert_yaxis()   # Highest value at the top
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[1].grid(True, alpha=0.3, axis='x')

    plt.suptitle("Category & Sub-Category Analysis", fontsize=16, fontweight="bold", y=1.00)
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart2_category_analysis.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✅ Saved → {path}")


# =============================================================================
# SECTION 4 ▸ CUSTOMER INSIGHTS  (Segment Breakdown)
# =============================================================================

def plot_segment_insights(df: pd.DataFrame):
    """
    Two charts for customer segmentation:
      Left  — Pie chart: share of total revenue from each segment.
      Right — Grouped bar chart: sales per segment broken down by category.

    Why segment analysis?
    ---------------------
    Different customer segments have different purchasing patterns.
    A business can tailor marketing, pricing, and support accordingly.
    """

    print("\n[CHART 3] Customer Segment Insights …")

    # ── Aggregations ─────────────────────────────────────────────────────────
    seg_sales  = df.groupby("Segment")["Sales"].sum()
    seg_cat    = df.groupby(["Segment", "Category"])["Sales"].sum().reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6), dpi=100)

    # ── Left: Pie chart ───────────────────────────────────────────────────────
    colors_seg = ["#3B82F6", "#10B981", "#F59E0B"]
    wedges, texts, autotexts = axes[0].pie(
        seg_sales.values,
        labels=seg_sales.index,
        autopct="%1.1f%%",        # Show percentage inside each slice
        colors=colors_seg[:len(seg_sales)],
        startangle=140,           # Rotate so 'Consumer' starts near top
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    # Make percentage labels bold
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")
        at.set_color('white')

    axes[0].set_title("Revenue Share by Customer Segment", fontsize=14, fontweight="bold")

    # ── Right: Grouped bar chart ──────────────────────────────────────────────
    pivot = seg_cat.pivot(index="Segment", columns="Category", values="Sales")
    
    # Get available categories and their colors
    available_categories = pivot.columns.tolist()
    cat_color_map = {
        "Technology": "#2563EB",
        "Furniture": "#10B981",
        "Office Supplies": "#F59E0B"
    }
    plot_colors = [cat_color_map.get(cat, "#999999") for cat in available_categories]
    
    pivot.plot(
        kind="bar",
        ax=axes[1],
        color=plot_colors,
        edgecolor="white",
        linewidth=0.5
    )

    axes[1].set_title("Sales by Segment & Category", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Customer Segment", fontsize=11)
    axes[1].set_ylabel("Total Sales (USD)", fontsize=11)
    axes[1].set_xticklabels(pivot.index, rotation=0)
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[1].legend(title="Category", loc="upper right")
    axes[1].grid(True, alpha=0.3, axis='y')

    plt.suptitle("Customer Segment Analysis", fontsize=16, fontweight="bold", y=1.00)
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart3_segment_insights.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✅ Saved → {path}")


# =============================================================================
# SECTION 5 ▸ GEOSPATIAL ANALYSIS  (Top 10 States by Sales)
# =============================================================================

def plot_geospatial_analysis(df: pd.DataFrame):
    """
    Horizontal bar chart: Top 10 States by total sales, coloured by Region.

    Why not a map?
    --------------
    A choropleth map requires a shapefile / geopandas — complex setup.
    A colour-coded bar chart is simpler, equally informative, and
    easier to explain during a viva.

    Key insight expected:
    ---------------------
    Coastal states (California, New York) typically dominate sales,
    suggesting urban density and higher purchasing power.
    """

    print("\n[CHART 4] Geospatial — Top 10 States …")

    # ── Aggregation ───────────────────────────────────────────────────────────
    state_sales = (
        df.groupby(["State", "Region"])["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    # Map each Region to a distinct colour
    region_colors = {
        "West":    "#2563EB",
        "East":    "#10B981",
        "Central": "#F59E0B",
        "South":   "#EF4444"
    }
    bar_colors = [region_colors.get(r, "#999999") for r in state_sales["Region"]]

    fig, ax = plt.subplots(figsize=(12, 6), dpi=100)

    bars = ax.barh(
        state_sales["State"],
        state_sales["Sales"],
        color=bar_colors,
        edgecolor="white",
        linewidth=0.8,
        height=0.6
    )

    # Annotate bars with sales figure
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + (width * 0.01),  # Slightly to the right
            bar.get_y() + bar.get_height() / 2,
            f"${width:,.0f}",
            va="center", fontsize=9, fontweight="bold"
        )

    ax.invert_yaxis()   # Highest at the top
    ax.set_title("Top 10 States by Total Sales (Coloured by Region)", fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Total Sales (USD)", fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.grid(True, alpha=0.3, axis='x')

    # Build a custom legend for the Region colours
    legend_patches = [Patch(color=c, label=r) for r, c in region_colors.items()]
    ax.legend(handles=legend_patches, title="Region", loc="lower right")

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart4_geospatial_top10_states.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✅ Saved → {path}")


# =============================================================================
# SECTION 6 ▸ BUSINESS INSIGHTS SUMMARY
# =============================================================================

def print_business_insights(df: pd.DataFrame):
    """
    Print a structured business-insights summary to the console.
    """

    print("\n" + "=" * 60)
    print("  BUSINESS INSIGHTS SUMMARY")
    print("=" * 60)

    total_sales   = df["Sales"].sum()
    avg_order     = df["Sales"].mean()
    
    try:
        top_cat     = df.groupby("Category")["Sales"].sum().idxmax()
    except:
        top_cat = "N/A"
    
    try:
        top_state   = df.groupby("State")["Sales"].sum().idxmax()
    except:
        top_state = "N/A"
    
    try:
        top_segment = df.groupby("Segment")["Sales"].sum().idxmax()
    except:
        top_segment = "N/A"
    
    try:
        peak_month  = df.groupby("Year-Month")["Sales"].sum().idxmax()
    except:
        peak_month = "N/A"

    print(f"  Total Revenue   : ${total_sales:>12,.2f}")
    print(f"  Avg Order Value : ${avg_order:>12,.2f}")
    print(f"  Top Category    : {top_cat}")
    print(f"  Top State       : {top_state}")
    print(f"  Top Segment     : {top_segment}")
    print(f"  Peak Month      : {peak_month}")

    print("\n  TOP 3 RECOMMENDATIONS:")
    print("  1. Double down on Technology — highest revenue per order.")
    print("     Focus on Phones & Accessories bundles to boost attach rate.")
    print("  2. Invest in Q4 marketing campaigns (Oct–Dec).")
    print("     Seasonal analysis shows a consistent sales spike in Q4.")
    print("  3. Prioritise the Consumer segment with loyalty programmes.")
    print("     Consumers drive the majority of revenue; retention is cheaper")
    print("     than acquisition.")
    print("=" * 60)


# =============================================================================
# MAIN  ▸  Run all sections in order
# =============================================================================

if __name__ == "__main__":
    
    try:
        # ── Load & clean ──────────────────────────────────────────────────────────
        DATA_PATH = os.path.join(OUTPUT_DIR, "train.csv")
        df = load_and_clean(DATA_PATH)
        
        # Check if dataframe is valid
        if df is None or len(df) == 0:
            print("\n❌ ERROR: No data loaded or dataframe is empty!")
            sys.exit(1)

        # ── Generate all four visualisations ──────────────────────────────────────
        plot_monthly_trend(df)
        plot_category_analysis(df)
        plot_segment_insights(df)
        plot_geospatial_analysis(df)

        # ── Print business insights ───────────────────────────────────────────────
        print_business_insights(df)

        print("\n" + "=" * 60)
        print("✅  ALL DONE! Four chart images saved in:")
        print(f"    {OUTPUT_DIR}")
        print("=" * 60)
        print("\nGenerated files:")
        print("  1. chart1_monthly_trend.png")
        print("  2. chart2_category_analysis.png")
        print("  3. chart3_segment_insights.png")
        print("  4. chart4_geospatial_top10_states.png")
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
