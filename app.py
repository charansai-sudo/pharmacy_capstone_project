
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="PharmaEasy Sales Dashboard",
    page_icon="💊",
    layout="wide"
)

from pathlib import Path

DB_FILE = Path("/content/pharmeasy.db")

MONTH_ORDER = [
    "2026-04",
    "2026-05",
    "2026-06"
]


# --------------------------------------------------
# LOAD DATA FROM SQLITE DATABASE
# --------------------------------------------------

@st.cache_data
def load_data():

    conn = sqlite3.connect(str(DB_FILE))

    query = """
    SELECT
        order_id,
        order_date,
        region,
        category,
        product,
        quantity,
        sales_inr,
        profit_inr
    FROM orders_clean
    WHERE order_date >= '2026-04-01'
      AND order_date < '2026-07-01'
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    df["order_date"] = pd.to_datetime(df["order_date"])

    df["month"] = df["order_date"].dt.strftime("%Y-%m")

    df["month"] = pd.Categorical(
        df["month"],
        categories=MONTH_ORDER,
        ordered=True
    )

    return df


df = load_data()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💊 PharmaEasy Sales Analytics Dashboard")

st.write(
    "April–June 2026 | Executive, Category and Regional Analysis"
)


# --------------------------------------------------
# REGION FILTER
# --------------------------------------------------

regions = ["All Regions"] + sorted(
    df["region"].dropna().unique()
)

selected_region = st.selectbox(
    "🌎 Select Region",
    regions
)


# Apply filter

if selected_region == "All Regions":

    filtered_df = df.copy()

else:

    filtered_df = df[
        df["region"] == selected_region
    ].copy()


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_sales = filtered_df["sales_inr"].sum()

total_profit = filtered_df["profit_inr"].sum()

# IMPORTANT:
# Count DISTINCT order IDs
# Do NOT use len(filtered_df)

total_orders = filtered_df["order_id"].nunique()


# --------------------------------------------------
# MONTHLY SALES
# --------------------------------------------------

april_sales = filtered_df.loc[
    filtered_df["month"] == "2026-04",
    "sales_inr"
].sum()

may_sales = filtered_df.loc[
    filtered_df["month"] == "2026-05",
    "sales_inr"
].sum()

june_sales = filtered_df.loc[
    filtered_df["month"] == "2026-06",
    "sales_inr"
].sum()


# April → May

if april_sales != 0:

    april_may_change = (
        (may_sales - april_sales)
        / april_sales
    ) * 100

else:

    april_may_change = 0


# May → June

if may_sales != 0:

    may_june_change = (
        (june_sales - may_sales)
        / may_sales
    ) * 100

else:

    may_june_change = 0


# --------------------------------------------------
# CATEGORY SUMMARY
# --------------------------------------------------

category_summary = (
    filtered_df
    .groupby("category")["sales_inr"]
    .sum()
    .sort_values(ascending=False)
)

top_category = category_summary.index[0]

top_category_sales = category_summary.iloc[0]


# --------------------------------------------------
# REGION SUMMARY
# --------------------------------------------------

region_summary = (
    filtered_df
    .groupby("region")["sales_inr"]
    .sum()
    .sort_values(ascending=False)
)


if selected_region == "All Regions":

    top_region = region_summary.index[0]

    top_region_sales = region_summary.iloc[0]

else:

    top_region = selected_region

    top_region_sales = total_sales


# ==================================================
# EXECUTIVE SUMMARY
# ==================================================

st.header("Executive Summary")

summary = (
    f"Total sales for April–June 2026 are "
    f"₹{total_sales:,.2f}, with total profit of "
    f"₹{total_profit:,.2f} across "
    f"{total_orders:,} distinct orders. "

    f"Sales changed by {april_may_change:+.2f}% "
    f"from April to May and by "
    f"{may_june_change:+.2f}% from May to June. "

    f"{top_category} is the largest category by sales "
    f"at ₹{top_category_sales:,.2f}, while "
    f"{top_region} represents the selected regional "
    f"sales view at ₹{top_region_sales:,.2f}. "

    f"Review the category and regional detail below "
    f"to identify the underlying order mix and sales movement."
)

st.info(summary)


# ==================================================
# LEVEL 1 — OVERVIEW
# ==================================================

st.header("1. Overview")


# KPI cards

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Sales (INR)",
        f"₹{total_sales:,.2f}"
    )


with col2:

    st.metric(
        "Total Profit (INR)",
        f"₹{total_profit:,.2f}"
    )


with col3:

    st.metric(
        "Distinct Order Count",
        f"{total_orders:,}"
    )


# --------------------------------------------------
# LINE CHART
# --------------------------------------------------

st.subheader(
    "📈 How do monthly sales change across regions?"
)


trend_df = (
    filtered_df
    .groupby(
        ["month", "region"],
        observed=True,
        as_index=False
    )["sales_inr"]
    .sum()
)


fig_line = px.line(
    trend_df,
    x="month",
    y="sales_inr",
    color="region",
    markers=True,
    title="How do monthly sales change across regions?",
    labels={
        "month": "Month",
        "sales_inr": "Sales (INR)",
        "region": "Region"
    }
)


# Start Y axis at zero

fig_line.update_yaxes(
    rangemode="tozero"
)


st.plotly_chart(
    fig_line,
    use_container_width=True
)


# --------------------------------------------------
# BAR CHART
# --------------------------------------------------

st.subheader(
    "📊 Which regions have the highest total sales?"
)


region_sales = (
    filtered_df
    .groupby(
        "region",
        as_index=False
    )["sales_inr"]
    .sum()
    .sort_values(
        "sales_inr",
        ascending=False
    )
)


fig_bar = px.bar(
    region_sales,
    x="region",
    y="sales_inr",
    title="Which regions have the highest total sales?",
    labels={
        "region": "Region",
        "sales_inr": "Total Sales (INR)"
    }
)


# Start Y axis at zero

fig_bar.update_yaxes(
    rangemode="tozero"
)


st.plotly_chart(
    fig_bar,
    use_container_width=True
)


# ==================================================
# LEVEL 2 — CATEGORY
# ==================================================

st.header("2. Category")


category_sales = (
    filtered_df
    .groupby(
        "category",
        as_index=False
    )["sales_inr"]
    .sum()
    .sort_values(
        "sales_inr",
        ascending=False
    )
)


# --------------------------------------------------
# DONUT CHART
# --------------------------------------------------

st.subheader(
    "🥧 What is the sales share of each medicine category?"
)


fig_donut = px.pie(
    category_sales,
    names="category",
    values="sales_inr",
    hole=0.45,
    title="What is the sales share of each medicine category?",
    labels={
        "category": "Medicine Category",
        "sales_inr": "Sales (INR)"
    }
)


st.plotly_chart(
    fig_donut,
    use_container_width=True
)


# Category table

category_display = category_sales.copy()

category_display["sales_inr"] = (
    category_display["sales_inr"]
    .map(lambda x: f"₹{x:,.2f}")
)


st.dataframe(
    category_display,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# LEVEL 3 — DETAIL
# ==================================================

st.header("3. Detail")


st.subheader(
    "What are the sales, profit and distinct orders by region and month?"
)


detail_df = (
    filtered_df
    .groupby(
        ["region", "month"],
        observed=True,
        as_index=False
    )
    .agg(
        total_sales=("sales_inr", "sum"),
        total_profit=("profit_inr", "sum"),
        distinct_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum")
    )
)


detail_df = detail_df.sort_values(
    ["region", "month"]
)


detail_display = detail_df.copy()


detail_display["total_sales"] = (
    detail_display["total_sales"]
    .map(lambda x: f"₹{x:,.2f}")
)


detail_display["total_profit"] = (
    detail_display["total_profit"]
    .map(lambda x: f"₹{x:,.2f}")
)


st.dataframe(
    detail_display,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "PharmaEasy Capstone Project | "
    "Source: orders_clean SQLite table"
)
