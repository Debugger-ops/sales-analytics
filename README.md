# 🛒 Superstore Sales — Exploratory Data Analysis Dashboard

> An interactive, multi-page data analytics dashboard built with Python and Streamlit,  
> analysing **9,800 real retail orders** to uncover sales trends, customer behaviour, shipping patterns,  
> and actionable business insights through rich, interactive visualisations.

**Team:** Vivek Pant · Yash · Param · Harishta  
**Course:** Data Analytics  
**Dataset:** Superstore Sales (`train.csv`) — a widely-used retail dataset from Kaggle

---

## 📁 Project Structure

```
ecommerce-sales-analysis/
│
├── app.py                               # Main Streamlit dashboard (7 pages)
├── eda_superstore.py                    # Standalone EDA script (static PNG charts)
├── train.csv                            # Superstore Sales dataset (9,800 orders)
│
├── chart1_monthly_trend.png             # Monthly sales trend line chart
├── chart2_category_analysis.png         # Category & sub-category bar charts
├── chart3_segment_insights.png          # Customer segment pie + grouped bar
├── chart4_geospatial_top10_states.png   # Top 10 states horizontal bar chart
│
├── Viva_Prep_Guide_Superstore_EDA.docx  # Viva Q&A guide (Word document)
└── README.md                            # This file
```

---

## 📊 Dataset Overview

| Field | Detail |
|---|---|
| Source file | `train.csv` |
| Total rows | 9,800 orders |
| Time period | January 2014 – December 2017 |
| Total revenue | $2,261,536 |
| Unique customers | 793 |
| Unique products | 1,849 |
| Geographies | 49 US states, 531 cities |
| Categories | Furniture · Office Supplies · Technology |
| Customer segments | Consumer · Corporate · Home Office |
| Shipping modes | Standard Class · Second Class · First Class · Same Day |

### Column Dictionary

| Column | Type | Description |
|---|---|---|
| Row ID | Integer | Unique row identifier |
| Order ID | String | Unique order reference |
| Order Date | Date | Date the order was placed (DD/MM/YYYY) |
| Ship Date | Date | Date the order was shipped |
| Ship Mode | String | Shipping speed selected by customer |
| Customer ID | String | Unique customer code |
| Customer Name | String | Full name of the customer |
| Segment | String | Customer segment (Consumer / Corporate / Home Office) |
| Country | String | Always "United States" |
| City | String | City where order was delivered |
| State | String | US State |
| Postal Code | Integer | ZIP code (11 missing — filled with 0) |
| Region | String | Geographic region (West / East / Central / South) |
| Product ID | String | Unique product code |
| Category | String | High-level product category |
| Sub-Category | String | 17 sub-categories (e.g. Phones, Chairs, Binders) |
| Product Name | String | Full product description |
| Sales | Float | Revenue in USD for that line item |

---

## 🚀 How to Run the Dashboard

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- A terminal / command prompt

### Step-by-step

```bash
# 1. Navigate to the project folder
cd "/Users/vivekpant0709/ecommerce-sales-analysis"

# 2. Create a virtual environment (only once)
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

# 4. Install required libraries (only once)
pip install streamlit plotly pandas openpyxl

# 5. Launch the dashboard
streamlit run app.py
```

Your browser will open automatically at **http://localhost:8501**

**Next time (skip steps 2 & 4):**
```bash
cd "/Users/vivekpant0709/ecommerce-sales-analysis"
source venv/bin/activate
streamlit run app.py
```

---

## 🖥️ Dashboard Pages — What Each One Shows

### 🏠 Page 1 — Overview
The landing page. Shows the big picture at a glance.
- **5 KPI cards:** Total Revenue, Total Orders, Average Order Value, Unique Customers, Products Sold
- **Sales Distribution Summary** (expandable): mean, median, standard deviation, IQR, percentiles, histogram
- **Revenue by Category** — horizontal bar chart (Furniture vs Office Supplies vs Technology)
- **Revenue by Region** — donut pie chart (West / East / Central / South)
- **Top 10 Products by Revenue** — horizontal bar chart colour-coded by category
- **Sample Orders table** — adjustable row count, with formatted currency and dates
- **Download CSV button** — exports the currently filtered dataset

### 📈 Page 2 — Trend Analysis
Explores how sales change over time.
- **Monthly Sales Line Chart** — shows every month from 2014–2017 with a shaded area fill
- **3-Month Rolling Average** — overlaid dashed red line to smooth out noise
- **Quarterly Breakdown** — grouped bar chart (Q1–Q4 per year side by side)
- **Year-over-Year Annual Sales** — bar chart showing growth year on year
- **Month-by-Month Cross-Year Comparison** — line chart with one line per year on the same Jan–Dec axis
- **Peak & Slowest Month** callout boxes

### 📦 Page 3 — Category Analysis
Deep-dives into product performance.
- **Sales by Category** & **Orders by Category** — horizontal bar charts
- **Top 10 Sub-Categories** — horizontal bar showing which sub-categories earn most
- **Category Treemap** — visual hierarchy (Category → Sub-Category → Sales area)
- **Sales Distribution Box Plot** — shows spread and outliers per category
- **Top N Products** table — adjustable with a slider (5–30 products)

### 👥 Page 4 — Customer Segments
Compares the three customer types.
- **3 KPI cards** for Consumer, Corporate, Home Office (revenue, orders, avg value)
- **Revenue Share Pie** — donut showing each segment's proportion of total revenue
- **Sales by Segment & Category** — grouped bar
- **Segment Sales Trend** — multi-line chart over time
- **Ship Mode Preference by Segment** — stacked bar
- **Top 5 Customers per Segment** — three mini-tables side by side

### 🗺️ Page 5 — Geospatial Analysis
Examines where sales come from geographically.
- **Top 15 States by Revenue** — horizontal bar, colour-coded by region
- **Revenue by Region Funnel** — shows West → East → Central → South ranking
- **Top 10 Cities** — horizontal bar with state hover info
- **Orders per State (Top 15)** — separate order-count bar
- **Full State-wise Table** — sortable table with Sales, Orders, Average per state

### 🚚 Page 6 — Shipping Analysis
Analyses delivery speed, cost patterns, and preferences.
- **4 KPI cards** — one per shipping mode (revenue, order count, avg value, avg days)
- **Orders per Ship Mode** — donut pie
- **Average Sales per Ship Mode** — horizontal bar
- **Average Shipping Days** — horizontal bar
- **Ship Mode by Category** — grouped bar
- **Shipping Days Distribution** — violin plot (shows full distribution shape + box + outliers)

### 💡 Page 7 — Business Insights
Summarises what the data tells us and what to do next.
- **6 st.metric boxes** — Top Category, Peak Month, Top Segment, Top State, Top Customer, Total Revenue
- **4 Quick-Fact KPI cards** — Top City, Top Sub-Category, Avg Ship Days, Monthly Avg Revenue
- **3 Recommendation Cards** — Q4 Campaign, Technology Up-Sells, Corporate Account Programme
- **Category × Segment Sunburst** — hierarchical proportion chart
- **Year × Month Heatmap** — colour-coded revenue grid (spot seasonal patterns instantly)
- **Top 10 Customers** — colour-gradient horizontal bar

---

## 🔧 Sidebar Filters

All filters apply globally across whichever page is open. Charts re-render instantly when any filter changes.

| Filter | Type | What it does |
|---|---|---|
| Year | Multi-select | Show only orders from selected years |
| Region | Multi-select | Restrict to chosen US regions |
| Category | Multi-select | Show only selected product categories |
| Segment | Multi-select | Filter by customer segment |
| Date From / To | Date pickers | Fine-grained date range within years |
| Customer search | Text input | Filter all data to orders matching the typed customer name |
| Download CSV | Button | Export the current filtered dataset as a CSV |

---

## 🧹 Data Cleaning Methodology

Cleaning was applied inside a `@st.cache_data` function so it runs only once and is cached for the session.

### Steps performed

1. **File loading** — `pd.read_csv()` with UTF-8 encoding. The code tries multiple possible paths automatically so it works regardless of the working directory.

2. **Date parsing** — `Order Date` and `Ship Date` were stored as strings (e.g. `"08/11/2017"`). The code tries three formats sequentially (`%d/%m/%Y`, `%m/%d/%Y`, `%Y-%m-%d`) and falls back to `infer_datetime_format` if none match. Rows with unparseable dates are dropped.

3. **Missing value handling** — `Postal Code` had 11 null entries (0.1% of data). Filled with `0` since this column is not used in any calculation or chart.

4. **Negative ship days** — A small number of rows had `Ship Date < Order Date` (data entry errors). These were clipped to 0 using `.clip(lower=0)`.

5. **Feature engineering** — New columns derived from existing data:
   - `Year-Month` — string like `"2017-11"` for monthly grouping
   - `Year` — integer year for filtering and annual charts
   - `Month Name` — abbreviated month string (`"Jan"`, `"Feb"`, …)
   - `Month Num` — integer 1–12 for correct month ordering
   - `Quarter` — string like `"Q4"` for quarterly grouping
   - `Ship Days` — integer, `(Ship Date − Order Date).days`

---

## 📈 Key Findings from the EDA

### Revenue & Orders
- Total revenue across all years: **$2,261,536**
- Total orders in the dataset: **9,800**
- Average order value: **~$230**

### Category Insights
- **Technology** earns the most revenue (~36%) with the highest average order value (~$456)
- **Office Supplies** has the most transactions (60% of orders) but the lowest avg value (~$119)
- **Furniture** sits in the middle — large individual items, fewer orders

### Top Sub-Categories
Phones, Chairs, and Storage consistently rank in the top 3 by revenue. Phones alone account for over $330,000.

### Time / Seasonality
- A **Q4 sales spike (Oct–Dec)** is visible in every single year — typically 30–80% above Q1
- **November** is the single best month, peaking at ~$118,000 in 2017
- **February** is consistently the weakest month

### Geography
- **California** is the #1 state ($446,306 in total sales)
- **New York** is #2 ($306,360)
- The **West region** generates the most revenue; **South** generates the least
- **Los Angeles** and **New York City** are the top two cities

### Customer Segments
- **Consumer** segment: ~50% of revenue, highest volume
- **Corporate** segment: fewer customers but ~30% higher average order value
- **Home Office**: smallest volume but growing steadily

### Shipping
- **Standard Class** accounts for ~60% of all orders
- **Same Day** shipping has the highest average sales value — customers who pay for speed buy more expensive items
- Average lead time: Standard 5 days → First Class 2 days → Same Day 0 days

---

## 💡 Top 3 Business Recommendations

### 1. 🚀 Launch a Dedicated Q4 Campaign
Every year without exception, sales spike 30–80% in October–December. The business should:
- Pre-position high-demand inventory (Phones, Chairs) by September
- Run email and discount campaigns in October
- Create Technology bundles for November's peak
- **Projected impact:** +10–15% annual revenue with minimal additional cost

### 2. 💻 Prioritise Technology Up-Sells
Technology has the highest revenue per order. Steps to increase it further:
- Train sales staff to recommend Accessories when a Phone or Machine is purchased
- Introduce bundle pricing (e.g. Laptop + Bag + Mouse at a 5% discount)
- **Projected impact:** A 5% improvement in attach rate = $25,000+ additional annual revenue

### 3. 🤝 Build a Corporate Account Programme
Corporate customers buy less often but spend more per order:
- Assign dedicated account managers to the top 30 corporate clients
- Offer tiered volume pricing for bulk orders
- Schedule quarterly business reviews
- **Projected impact:** Improving Corporate retention by 20% = $60,000+ additional annual revenue

---

## 🛠️ Tech Stack — Libraries & Their Roles

| Library | Version | Purpose in This Project |
|---|---|---|
| **Python** | 3.8+ | Core programming language |
| **pandas** | latest | Data loading (`read_csv`), cleaning, filtering, grouping (`groupby`), aggregation (`agg`, `sum`, `mean`), pivot tables |
| **Streamlit** | latest | Entire web app framework — sidebar, pages, widgets (`st.radio`, `st.multiselect`, `st.slider`, `st.date_input`), layout (`st.columns`), caching (`@st.cache_data`) |
| **Plotly Express** | latest | High-level interactive charts — bar, pie, line, treemap, sunburst, imshow (heatmap), box, violin, histogram, funnel |
| **Plotly Graph Objects** | latest | Low-level chart customisation — used for the monthly trend chart with custom fill and the rolling average overlay |
| **io** | stdlib | In-memory byte buffer for the CSV download button (no temp file needed) |
| **os** | stdlib | Cross-platform file path resolution so `train.csv` is found regardless of how the script is launched |

### Why Streamlit over Flask / Django?
Streamlit is purpose-built for data science dashboards. A single Python script becomes a full interactive web app with zero HTML, CSS (beyond custom overrides), or JavaScript required. It re-runs automatically when a widget changes, making reactive filtering trivial.

### Why Plotly over Matplotlib?
Plotly charts are interactive — users can hover for exact values, click to filter legends, zoom, and pan. Matplotlib produces static images. For a dashboard meant to be explored, Plotly is the better choice.

---

## 🎓 Viva Preparation — Expected Questions & Answers

### Q1: What is EDA and why did you do it?
**A:** Exploratory Data Analysis (EDA) is the process of summarising and visualising a dataset to understand its structure, spot patterns, detect anomalies, and form hypotheses — *before* building any model. We did it to understand how Superstore's revenue is distributed across time, geography, category, and customer type, so we could make data-driven business recommendations.

### Q2: How did you handle missing values?
**A:** Only the `Postal Code` column had missing values — 11 out of 9,800 rows (0.1%). We filled them with `0` using `fillna(0)` because this column wasn't used in any analysis. Rows with missing or unparseable `Order Date` or `Ship Date` were dropped since dates are fundamental to all time-based charts.

### Q3: What is `@st.cache_data` and why did you use it?
**A:** `@st.cache_data` is a Streamlit decorator that stores the return value of a function in memory after the first call. When the user changes a filter or navigates between pages, Streamlit re-runs the script — without the cache, `load_data()` would re-read and re-clean the CSV every single time, which is slow. The cache makes the app feel instant after the first load.

### Q4: What does `groupby` do in pandas?
**A:** `groupby` splits the DataFrame into groups based on one or more columns, then you apply an aggregation function (like `sum()`, `mean()`, `count()`) to each group. For example, `df.groupby("Category")["Sales"].sum()` splits by category and totals the Sales column for each group, giving us revenue by category.

### Q5: What is a rolling average and why did you add it?
**A:** A rolling (moving) average smooths a time series by replacing each point with the average of the surrounding N points. We used a 3-month rolling average on the monthly trend chart. This removes month-to-month noise so the underlying trend (is the business growing or shrinking?) is easier to see.

### Q6: What is the difference between `.mean()` and `.median()`? Which is more useful here?
**A:** `.mean()` is the arithmetic average — sensitive to extreme values (outliers). `.median()` is the middle value when sorted — resistant to outliers. Sales data is heavily right-skewed (most orders are small but a few are very large), so the **median** is a more representative "typical" order value. The mean is inflated by high-value Technology orders.

### Q7: Why does the Q4 sales spike happen every year?
**A:** Consumer spending peaks in Q4 due to seasonal factors: back-to-school buying in August/September, Halloween, Thanksgiving (major US shopping event), Black Friday, Cyber Monday, and Christmas gifting all drive purchases. Office Supplies and Technology (commonly given as gifts or bought on sale) benefit most.

### Q8: What is a treemap? Why is it useful here?
**A:** A treemap displays hierarchical data as nested rectangles. The area of each rectangle is proportional to its value. Here we used it to show Category → Sub-Category → Sales in one compact visual. It makes it immediately obvious that Phones within Technology and Chairs within Furniture are the dominant sub-categories, without needing a long table.

### Q9: What is a violin plot? How does it differ from a box plot?
**A:** A box plot shows the median, IQR (25th–75th percentile), and whiskers (range), with outlier dots. A violin plot adds a kernel density curve (the shape of the "violin") which shows *where* values are concentrated within the range — not just the quartiles. We used it for shipping days distribution to show that Standard Class clusters around 4–6 days while Same Day clusters at 0.

### Q10: Why did you use Plotly instead of Matplotlib?
**A:** Plotly produces interactive charts — users can hover to see exact values, zoom, pan, click legend items to toggle series, and download charts as PNGs. Matplotlib is great for static publication-quality figures but unsuitable for an interactive dashboard. The `eda_superstore.py` script still uses Matplotlib/Seaborn for the static PNG charts.

### Q11: What is the purpose of the sidebar filters?
**A:** The sidebar filters are global — they apply to every chart on every page simultaneously. They let the user drill into subsets of the data (e.g. "show me only Technology orders in the West region in 2016") without changing the code. Streamlit re-runs the entire script when a widget changes, so all charts update automatically.

### Q12: What does `pd.to_datetime()` do?
**A:** It converts a column of date strings (like `"08/11/2017"`) into Python `datetime` objects. Once a column is in datetime format, pandas can extract `.dt.year`, `.dt.month`, `.dt.quarter`, and calculate differences between dates (like `Ship Date - Order Date` for shipping days). Without this conversion the dates would just be strings and no time-based analysis would be possible.

### Q13: What is the IQR and how is it calculated?
**A:** IQR stands for Interquartile Range. It is the difference between the 75th percentile (Q3) and the 25th percentile (Q1): `IQR = Q3 − Q1`. It represents the middle 50% of the data and is used as a robust measure of spread that is unaffected by extreme values. A large IQR means high variability in order values.

### Q14: How does the customer search filter work technically?
**A:** We use pandas' `str.contains()` method: `fdf[fdf["Customer Name"].str.contains(search_term, case=False, na=False)]`. This is a case-insensitive substring search — typing "claire" will match "Claire Gute". The `na=False` ensures null names don't raise errors.

### Q15: What would you do next to extend this project?
**A:** Several extensions are possible:
- **Profit margin analysis** — if a Profit column were available, we could identify loss-making orders
- **Predictive modelling** — use Prophet or ARIMA to forecast next quarter's revenue
- **Customer segmentation (RFM analysis)** — score customers by Recency, Frequency, Monetary value to identify VIPs vs at-risk customers
- **Anomaly detection** — flag unusually large or small orders automatically
- **Deployment** — host on Streamlit Cloud or AWS so external stakeholders can access it

---

## 🧪 How to Run the Static EDA Script

If you just want to regenerate the four PNG charts without launching the dashboard:

```bash
python3 eda_superstore.py
```

This will save `chart1_monthly_trend.png`, `chart2_category_analysis.png`, `chart3_segment_insights.png`, and `chart4_geospatial_top10_states.png` into the project folder.

---

## 📄 Additional Resources

- **`Viva_Prep_Guide_Superstore_EDA.docx`** — Word document with 10 examiner Q&As, methodology notes, and a quick-reference revision card
- **Streamlit docs:** https://docs.streamlit.io
- **Plotly docs:** https://plotly.com/python
- **pandas docs:** https://pandas.pydata.org/docs
- **Dataset origin:** Superstore Sales (Kaggle) — a standard retail EDA teaching dataset

---

## 🙋 About This Project

This project was created as part of a Data Analytics college course. The goal was to perform a **comprehensive Exploratory Data Analysis** on the Superstore Sales dataset and present findings through an interactive, filterable dashboard.

The project covers:
- Data ingestion and cleaning with pandas
- Feature engineering (time-based columns, derived metrics)
- Time-series trend analysis with seasonality detection
- Category and product performance benchmarking
- Customer segmentation analysis
- Geographic sales distribution
- Shipping behaviour analysis
- Actionable business recommendations backed by data

---

*Built with Python · Streamlit · Plotly · pandas*  
*Vivek Pant · Yash · Param · Harishta · 2024*
