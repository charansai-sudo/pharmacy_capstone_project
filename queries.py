
import sqlite3
import pandas as pd

DB_FILE = "/content/pharmeasy.db"


def run_query(conn, sql):
    return pd.read_sql_query(sql, conn)


def main():
    conn = sqlite3.connect(DB_FILE)

    print("=" * 60)
    print("PHARMEASY SQL ANALYSIS")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. LEFT JOIN validation
    # ---------------------------------------------------------
    left_join_sql = """
        SELECT
            r.region,
            COUNT(*) AS row_count,
            COUNT(o.order_id) AS matched_orders
        FROM regions_master r
        LEFT JOIN orders_clean o
            ON r.region = o.region
        GROUP BY r.region
        ORDER BY r.region;
    """

    left_join = run_query(conn, left_join_sql)

    print("\n1. LEFT JOIN VALIDATION")
    print(left_join.to_string(index=False))

    print("\nLEFT JOIN total rows:", left_join["row_count"].sum())
    print("Matched orders:", left_join["matched_orders"].sum())

    # ---------------------------------------------------------
    # 2. INNER JOIN validation
    # ---------------------------------------------------------
    inner_join_sql = """
        SELECT
            r.region,
            COUNT(o.order_id) AS order_count
        FROM regions_master r
        INNER JOIN orders_clean o
            ON r.region = o.region
        GROUP BY r.region
        ORDER BY r.region;
    """

    inner_join = run_query(conn, inner_join_sql)

    print("\n2. INNER JOIN VALIDATION")
    print(inner_join.to_string(index=False))

    print("\nINNER JOIN total orders:",
          inner_join["order_count"].sum())

    # ---------------------------------------------------------
    # 3. Duplicate order_id validation
    # ---------------------------------------------------------
    duplicate_sql = """
        SELECT
            order_id,
            COUNT(*) AS duplicate_count
        FROM orders_clean
        GROUP BY order_id
        HAVING COUNT(*) > 1;
    """

    duplicates = run_query(conn, duplicate_sql)

    print("\n3. DUPLICATE ORDER ID CHECK")
    print("Duplicate order IDs:", len(duplicates))

    # ---------------------------------------------------------
    # 4. Order count by region
    # ---------------------------------------------------------
    region_orders_sql = """
        SELECT
            region,
            COUNT(DISTINCT order_id) AS distinct_orders
        FROM orders_clean
        GROUP BY region
        ORDER BY distinct_orders DESC;
    """

    region_orders = run_query(conn, region_orders_sql)

    print("\n4. DISTINCT ORDERS BY REGION")
    print(region_orders.to_string(index=False))

    # ---------------------------------------------------------
    # 5. Region x Month sales
    # ---------------------------------------------------------
    monthly_sales_sql = """
        SELECT
            region,
            strftime('%Y-%m', order_date) AS month,
            ROUND(SUM(sales_inr), 2) AS total_sales,
            ROUND(SUM(profit_inr), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS distinct_orders
        FROM orders_clean
        GROUP BY region, month
        ORDER BY region, month;
    """

    monthly_sales = run_query(conn, monthly_sales_sql)

    print("\n5. REGION × MONTH SALES")
    print(monthly_sales.to_string(index=False))

    # ---------------------------------------------------------
    # 6. Overall monthly sales
    # ---------------------------------------------------------
    overall_monthly_sql = """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            ROUND(SUM(sales_inr), 2) AS total_sales,
            ROUND(SUM(profit_inr), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS distinct_orders
        FROM orders_clean
        GROUP BY month
        ORDER BY month;
    """

    overall_monthly = run_query(conn, overall_monthly_sql)

    print("\n6. OVERALL MONTHLY METRICS")
    print(overall_monthly.to_string(index=False))

    # ---------------------------------------------------------
    # 7. Guntur April → May validation
    # ---------------------------------------------------------
    guntur_sql = """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            ROUND(SUM(sales_inr), 2) AS total_sales
        FROM orders_clean
        WHERE region = 'Guntur'
        GROUP BY month
        ORDER BY month;
    """

    guntur = run_query(conn, guntur_sql)

    print("\n7. GUNTUR MONTHLY SALES")
    print(guntur.to_string(index=False))

    if len(guntur) >= 2:
        april = guntur.loc[
            guntur["month"] == "2026-04",
            "total_sales"
        ].iloc[0]

        may = guntur.loc[
            guntur["month"] == "2026-05",
            "total_sales"
        ].iloc[0]

        mom = ((may - april) / april) * 100

        print(f"\nGuntur April sales: ₹{april:,.2f}")
        print(f"Guntur May sales: ₹{may:,.2f}")
        print(f"Guntur April → May MoM: {mom:.2f}%")

    conn.close()


if __name__ == "__main__":
    main()
