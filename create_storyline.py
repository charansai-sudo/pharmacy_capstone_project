
import sqlite3
import pandas as pd

DB_FILE = "/content/pharmeasy.db"

conn = sqlite3.connect(DB_FILE)

# -----------------------------
# Guntur monthly sales
# -----------------------------
guntur_monthly = pd.read_sql_query("""
SELECT
    strftime('%Y-%m', order_date) AS month,
    SUM(sales_inr) AS sales
FROM orders_clean
WHERE region = 'Guntur'
  AND order_date >= '2026-04-01'
  AND order_date < '2026-06-01'
GROUP BY month
ORDER BY month
""", conn)

april_sales = guntur_monthly.loc[
    guntur_monthly["month"] == "2026-04",
    "sales"
].iloc[0]

may_sales = guntur_monthly.loc[
    guntur_monthly["month"] == "2026-05",
    "sales"
].iloc[0]

mom_change = ((may_sales - april_sales) / april_sales) * 100


# -----------------------------
# Guntur May category
# -----------------------------
guntur_category = pd.read_sql_query("""
SELECT
    category,
    SUM(sales_inr) AS sales
FROM orders_clean
WHERE region = 'Guntur'
  AND order_date >= '2026-05-01'
  AND order_date < '2026-06-01'
GROUP BY category
ORDER BY sales DESC
""", conn)

top_category = guntur_category.iloc[0]["category"]
top_category_sales = guntur_category.iloc[0]["sales"]


# -----------------------------
# Guntur distinct orders
# -----------------------------
guntur_orders = pd.read_sql_query("""
SELECT
    COUNT(DISTINCT order_id) AS order_count
FROM orders_clean
WHERE region = 'Guntur'
  AND order_date >= '2026-04-01'
  AND order_date < '2026-06-01'
""", conn)

guntur_order_count = int(guntur_orders.iloc[0]["order_count"])

conn.close()


# -----------------------------
# Presentation storyline
# -----------------------------
storyline = f"""# PharmaEasy Presentation Storyline

## 1. Executive SCR — Situation, Complication, Resolution

### Situation

Guntur recorded April 2026 sales of ₹{april_sales:,.2f} and May 2026 sales of ₹{may_sales:,.2f}, producing a Month-on-Month change of +{mom_change:.2f}%.

### Complication

The April-to-May movement of +{mom_change:.2f}% is above the configured 8% operational-alert threshold. The percentage identifies a significant movement in the observed sales data, but the percentage alone does not establish why the movement occurred.

### Resolution

Review Guntur's April and May order-level records by category, product, quantity, distinct order count and sales value. Use the dashboard's Category and Detail views during the next review checkpoint before drawing a causal business explanation.


## 2. Regional Manager OCD — Overview, Category, Detail

### Overview

Guntur's April-to-May sales movement was +{mom_change:.2f}%, increasing from ₹{april_sales:,.2f} in April to ₹{may_sales:,.2f} in May.

### Category

In May 2026, {top_category} was Guntur's largest sales category at ₹{top_category_sales:,.2f}. This identifies the largest observed category contribution in the May Guntur data, but it does not by itself establish that the category caused the overall April-to-May change.

### Detail

The supporting Guntur data contains monthly sales, profit, quantity and distinct-order measures.

The Guntur April-to-May calculation uses:

(May Sales − April Sales) / April Sales × 100

The dashboard provides the regional, monthly, category and detail views required for further review.


## 3. Anticipated Stakeholder Pushback Q&A

### Q1. Why should I believe this number?

**1 — Acknowledge the concern**

It is reasonable to ask whether the +{mom_change:.2f}% Guntur movement can be traced back to the underlying records.

**2 — Verified vs. not verified**

The April sales of ₹{april_sales:,.2f}, May sales of ₹{may_sales:,.2f}, and resulting +{mom_change:.2f}% calculation are directly derived from the `orders_clean` database records. The calculation verifies the observed movement, but it does not by itself verify the business reason behind that movement.

**3 — Resolve uncertainty and by when**

Reconcile Guntur's April and May order-level records by order ID, category, product, quantity and sales value by the next review checkpoint, within one business day.


### Q2. What if an alternative explanation is driving this?

**1 — Acknowledge the concern**

An alternative explanation could account for the observed sales movement, and the aggregate percentage alone cannot distinguish between possible explanations.

**2 — Verified vs. not verified**

The dataset verifies the observed sales movement and its calculation. It does not independently verify external factors or establish causation from the aggregate result alone.

**3 — Resolve uncertainty and by when**

Compare April and May Guntur order mix by category, product, quantity and distinct order count by the next review checkpoint, within one business day. Any explanation not supported by those records should remain a hypothesis.


### Q3. What did you not check?

**1 — Acknowledge the concern**

The current finding is an aggregate regional sales comparison, so additional order-level checks are relevant.

**2 — Verified vs. not verified**

The April and May sales totals and the Month-on-Month calculation are verified from `orders_clean`. The current finding does not by itself establish which individual products or order groups explain the movement.

**3 — Resolve uncertainty and by when**

Use the dashboard's Detail and Category views to inspect Guntur by month, category, product and distinct order count by the next review checkpoint, within one business day.


### Q4. What would change your recommendation?

**1 — Acknowledge the concern**

It is reasonable to ask what evidence would make us change the recommendation to investigate the Guntur increase further.

**2 — Verified vs. not verified**

The +{mom_change:.2f}% movement is verified from the cleaned order records. The recommendation would need to change if the underlying order-level validation showed that the increase resulted from a data-quality issue, duplicate records, incorrect sales values, or another confirmed measurement problem.

**3 — Resolve uncertainty and by when**

Reconcile the relevant Guntur order records and validation checks by the next review checkpoint, within one business day. If a material data-quality issue is confirmed, correct the data and rerun the analysis before making a business recommendation.
"""


# -----------------------------
# Save file
# -----------------------------
with open("/content/presentation_storyline.md", "w", encoding="utf-8") as f:
    f.write(storyline)

print("✅ presentation_storyline.md created successfully")
print()
print(f"April sales: ₹{april_sales:,.2f}")
print(f"May sales: ₹{may_sales:,.2f}")
print(f"MoM change: +{mom_change:.2f}%")
print(f"Top May category: {top_category}")
print(f"Top category sales: ₹{top_category_sales:,.2f}")
print(f"Guntur distinct orders: {guntur_order_count}")
