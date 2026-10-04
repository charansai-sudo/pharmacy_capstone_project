
# PharmaEasy — Data Quality Report

## 1. Dataset Overview

| Metric | Value |
|---|---:|
| Raw rows | 2159 |
| Cleaned rows | 2100 |
| Duplicate rows removed | 59 |
| Missing categories imputed | 48 |
| Missing profit values imputed | 94 |
| Final duplicate order IDs | 0 |
| Final missing categories | 0 |
| Final missing profit values | 0 |

## 2. Schema

The final cleaned dataset contains these columns:

- `order_id`
- `order_date`
- `region`
- `category`
- `product`
- `quantity`
- `sales_inr`
- `profit_inr`

## 3. Cleaning Steps

1. Loaded the raw PharmaEasy orders dataset.
2. Validated the required schema.
3. Removed duplicate records using `order_id`.
4. Standardized `order_date` into `YYYY-MM-DD` format.
5. Filled missing category values using the most common category.
6. Filled missing profit values using the median profit.
7. Converted quantity, sales, and profit fields to numeric values.
8. Validated the final cleaned dataset.
9. Saved the result as `orders_clean.csv`.

## 4. Validation Results

The final dataset passed the following checks:

- Required columns are present.
- `order_id` contains no duplicates.
- Category values contain no missing values.
- Profit values contain no missing values.
- Date values are standardized.
- Numeric fields are converted to numeric types.

## 5. Data Coverage

The dataset covers the April–June 2026 analysis period.

The project contains six product categories:

- Lab Tests
- Medical Devices
- OTC Medicines
- Personal Care
- Prescription Medicines
- Wellness & Nutrition

The region master contains 10 regions. The cleaned orders contain transactions for 9 of those regions.

## 6. Assumptions

- Duplicate `order_id` records are treated as duplicate orders and only the first record is retained.
- Missing category values are replaced with the dataset mode.
- Missing profit values are replaced with the dataset median.
- `sales_inr` and `profit_inr` represent monetary values in Indian Rupees.
- The cleaned dataset is used as the source for downstream SQL analysis and dashboard metrics.

## 7. Quality Conclusion

The cleaned dataset contains **2100 valid order records** and passes the required schema, duplicate, missing-value, and datatype validation checks.

This dataset is suitable for the downstream database, SQL analysis, metrics engine, reporting, and Streamlit dashboard.
