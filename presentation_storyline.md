# PharmaEasy Presentation Storyline

## 1. Executive SCR — Situation, Complication, Resolution

### Situation

Guntur recorded April 2026 sales of ₹62,442.27 and May 2026 sales of ₹138,738.93, producing a Month-on-Month change of +122.19%.

### Complication

The April-to-May movement of +122.19% is above the configured 8% operational-alert threshold. The percentage identifies a significant movement in the observed sales data, but the percentage alone does not establish why the movement occurred.

### Resolution

Review Guntur's April and May order-level records by category, product, quantity, distinct order count and sales value. Use the dashboard's Category and Detail views during the next review checkpoint before drawing a causal business explanation.


## 2. Regional Manager OCD — Overview, Category, Detail

### Overview

Guntur's April-to-May sales movement was +122.19%, increasing from ₹62,442.27 in April to ₹138,738.93 in May.

### Category

In May 2026, Wellness & Nutrition was Guntur's largest sales category at ₹53,085.01. This identifies the largest observed category contribution in the May Guntur data, but it does not by itself establish that the category caused the overall April-to-May change.

### Detail

The supporting Guntur data contains monthly sales, profit, quantity and distinct-order measures.

The Guntur April-to-May calculation uses:

(May Sales − April Sales) / April Sales × 100

The dashboard provides the regional, monthly, category and detail views required for further review.


## 3. Anticipated Stakeholder Pushback Q&A

### Q1. Why should I believe this number?

**1 — Acknowledge the concern**

It is reasonable to ask whether the +122.19% Guntur movement can be traced back to the underlying records.

**2 — Verified vs. not verified**

The April sales of ₹62,442.27, May sales of ₹138,738.93, and resulting +122.19% calculation are directly derived from the `orders_clean` database records. The calculation verifies the observed movement, but it does not by itself verify the business reason behind that movement.

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

The +122.19% movement is verified from the cleaned order records. The recommendation would need to change if the underlying order-level validation showed that the increase resulted from a data-quality issue, duplicate records, incorrect sales values, or another confirmed measurement problem.

**3 — Resolve uncertainty and by when**

Reconcile the relevant Guntur order records and validation checks by the next review checkpoint, within one business day. If a material data-quality issue is confirmed, correct the data and rerun the analysis before making a business recommendation.
