# Title

Guntur Region — April→May 2026 Sales Swing [HIGH]

# Context

The Guntur region recorded a +122.19% Month-on-Month change in total sales from April 2026 to May 2026 [HIGH]. This is the single largest-magnitude flagged change in the dataset [HIGH].

# Key Insight

Guntur's sales increased from ₹62,442.27 in April 2026 to ₹138,738.93 in May 2026 [HIGH]. The +122.19% change exceeds the 8% operational-alert threshold [HIGH] and warrants a closer review of the underlying order data [MEDIUM].

# Evidence

- Region: Guntur [HIGH]
- April 2026 sales: ₹62,442.27 [HIGH]
- May 2026 sales: ₹138,738.93 [HIGH]
- April→May MoM change: +122.19% [HIGH]
- The change is calculated as (May sales − April sales) / April sales × 100 [LOW].
- Guntur was flagged by flag_significant_regions_v1(threshold=8) [HIGH].

# Recommendation

Review Guntur's April and May order-level records, including order counts, quantities, product categories, and sales values, to identify which observed changes in the dataset account for the +122.19% movement [MEDIUM].

# Next Check

Compare Guntur's May 2026 order mix with April 2026 by category and product, and check whether the May increase is concentrated in a small number of orders, products, or categories [MEDIUM].

# Assumptions

No external market factors are assumed [LOW]. Any explanation for the increase is only a hypothesis until it is supported by the order-level data [LOW]. The 8% threshold is treated as an operational alert for human review, not as statistical proof of an underlying structural change [LOW].
