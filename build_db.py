
import sqlite3
import pandas as pd

ORDERS_FILE = "/content/orders_clean.csv"
REGIONS_FILE = "/content/regions_master.csv"
DB_FILE = "/content/pharmeasy.db"


def build_database():
    orders = pd.read_csv(ORDERS_FILE)
    regions = pd.read_csv(REGIONS_FILE)

    conn = sqlite3.connect(DB_FILE)

    # Rebuild the project tables
    orders.to_sql("orders_clean", conn, if_exists="replace", index=False)
    regions.to_sql("regions_master", conn, if_exists="replace", index=False)

    # Create useful indexes
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_orders_order_id
        ON orders_clean(order_id)
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_orders_region
        ON orders_clean(region)
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_orders_order_date
        ON orders_clean(order_date)
    """)

    conn.commit()

    # Validate database
    orders_count = conn.execute(
        "SELECT COUNT(*) FROM orders_clean"
    ).fetchone()[0]

    regions_count = conn.execute(
        "SELECT COUNT(*) FROM regions_master"
    ).fetchone()[0]

    print("PharmaEasy SQLite Database")
    print("=" * 40)
    print(f"Database: {DB_FILE}")
    print(f"orders_clean rows: {orders_count}")
    print(f"regions_master rows: {regions_count}")

    conn.close()


if __name__ == "__main__":
    build_database()
