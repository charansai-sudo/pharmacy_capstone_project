
import pandas as pd
import numpy as np

RAW_FILE = "/content/pharmeasy_orders_raw.csv"
REGIONS_FILE = "/content/regions_master.csv"

SEED = 42

np.random.seed(SEED)

# Read the existing deterministic raw dataset
orders = pd.read_csv(RAW_FILE)
regions = pd.read_csv(REGIONS_FILE)

print("PharmaEasy deterministic dataset")
print("=" * 40)
print(f"Random seed: {SEED}")
print(f"Raw orders: {len(orders)}")
print(f"Regions master: {len(regions)}")
print()
print("Columns:")
print(list(orders.columns))
