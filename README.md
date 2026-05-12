# 🛒 Superstore Sales — Exploratory Data Analysis Dashboard

> An interactive data analytics dashboard built with Python & Streamlit, analysing 9,800 real retail orders to uncover sales trends, customer behaviour, and business insights.

**Author:** vivek | **Course:** Data Analytics | **Dataset:** Superstore Sales (train.csv)

---

## 📁 Project Structure

```
ecommerce-sales-analysis/
│
├── app.py                          # Main Streamlit dashboard application
├── eda_superstore.py               # Standalone EDA script (generates static charts)
├── train.csv                       # Superstore Sales dataset (9,800 orders)
│
├── chart1_monthly_trend.png        # Monthly sales trend line chart
├── chart2_category_analysis.png    # Category & sub-category bar charts
├── chart3_segment_insights.png     # Customer segment pie + grouped bar
├── chart4_geospatial_top10_states.png  # Top 10 states horizontal bar chart
│
├── Viva_Prep_Guide_Superstore_EDA.docx  # Viva Q&A guide (Word document)
└── README.md                       # This file
```

---

## 📊 Dataset Overview

| Field | Detail |
|---|---|
| File | `train.csv` |
| Rows | 9,800 orders |
| Period | 2014 – 2018 |
| Total Revenue | $2,261,536.78 |
| Unique Customers | 793 |
| Unique Products | 1,849 |

**Columns:** Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales

---

## 🚀 How to Run

### Step 1 — Go to the project folder
```bash
cd "/Users/vivekpant0709/ecommerce-sales-analysis"
```

### Step 2 — Create a virtual environment
```bash
python3 -m venv venv
```

### Step 3 — Activate it
```bash
source venv/bin/activate
```
> On Windows: `venv\Scripts\activate`

### Step 4 — Install dependencies
```bash
pip install streamlit plotly pandas
```

### Step 5 — Launch the dashboard
```bash
streamlit run app.py
```

Your browser will open automatically at **http://localhost:8501**

### Next time (skip Steps 2 & 4)
```bash
cd "/Users/vivekpant0709/ecommerce-sales-analysis"
source venv/bin/activate
streamlit run app.py
```

---

## 🖥️ Dashboard Pages

| Page | What It Shows |
|---|---|
| 🏠 Overview | KPI cards (Revenue, Orders, Customers, Products), category & region charts, data table |
| 📈 Trend Analysis | Monthly sales line chart, quarterly breakdown, year-over-year comparison |
| 📦 Category Analysis | Revenue by category, top 10 sub-categories, treemap, best-selling products |
| 👥 Customer Segments | Segment KPIs, revenue share pie, category breakdown, ship mode preferences |
| 🗺️ Geospatial Analysis | Top 15 states, regional funnel chart, top 10 cities, full state table |
| 🚚 Shipping Analysis | Ship mode revenue, avg delivery days, category-wise ship mode usage |
| 💡 Business Insights | Key metrics, 3 recommendations, sunburst chart, heatmap, top customers |

The sidebar lets you filter all pages by **Year**, **Region**, **Category**, and **Segment** — all charts update instantly.

---

## 🧹 Data Cleaning Steps

1. **Loaded** `train.csv` using `pandas.read_csv()`
2. **Parsed dates** — `Order Date` and `Ship Date` converted from DD/MM/YYYY strings using `pd.to_datetime(..., dayfirst=True)`
3. **Handled missing values** — 11 missing `Postal Code` entries filled with `0` (column not used in analysis)
4. **Engineered features:**
   - `Year-Month` — monthly period for time-series grouping
   - `Year`, `Month Name`, `Quarter` — for time-based filtering and charts
   - `Ship Days` — delivery lead time calculated as `Ship Date - Order Date`

---

## 📈 Key Findings

- **Technology** is the top revenue category with the highest average order value
- **November 2018** was the single best-performing month
- **California** leads all states in total sales
- **Consumers** make up ~50% of revenue; **Corporate** orders have higher average values
- A consistent **Q4 sales spike** (Oct–Dec) appears every year — driven by seasonal demand
- **Standard Class** is the most-used shipping mode; **Same Day** has the highest avg order value

---

## 💡 Top 3 Business Recommendations

1. **Launch a Q4 Campaign** — Sales spike 30–80% every Oct–Dec. Pre-position stock in September and run targeted campaigns to capitalise on the seasonal window.
2. **Prioritise Technology Up-Sells** — Highest revenue per order. Bundle Phones with Accessories to increase attach rate and average order value.
3. **Build a Corporate Account Programme** — Assign dedicated account managers to top corporate clients and offer volume-pricing tiers to boost retention and lifetime value.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core programming language |
| pandas | Data loading, cleaning, and aggregation |
| Streamlit | Interactive web dashboard (frontend + backend) |
| Plotly Express | Interactive charts and visualisations |
| Matplotlib / Seaborn | Static chart generation (`eda_superstore.py`) |
| python-docx | Viva prep guide Word document generation |

---

## 📄 Additional Files

- **`eda_superstore.py`** — Run this standalone to regenerate the 4 static PNG charts without the dashboard:
  ```bash
  python3 eda_superstore.py
  ```

- **`Viva_Prep_Guide_Superstore_EDA.docx`** — Word document with 10 examiner Q&As, methodology notes, business recommendations, and a quick-reference revision card for the viva.

---

## 🙋 About

This project was created as part of a Data Analytics college course. The goal was to perform a comprehensive EDA on the Superstore Sales dataset and present findings through an interactive dashboard, covering data cleaning, time-series analysis, category and segment breakdowns, geospatial insights, and actionable business recommendations.
