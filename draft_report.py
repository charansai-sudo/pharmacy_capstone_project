
import json
from datetime import datetime


def draft_report_v1(metrics):
    """
    Create a Context–Insight–Implication report.

    Required metrics:
        region
        previous_month_sales
        current_month_sales
        mom_change_pct
    """

    required = [
        "region",
        "previous_month_sales",
        "current_month_sales",
        "mom_change_pct"
    ]

    missing = [
        key for key in required
        if key not in metrics or metrics[key] is None
    ]

    if missing:
        raise ValueError(
            f"Missing required metrics: {missing}"
        )

    region = metrics["region"]
    previous = metrics["previous_month_sales"]
    current = metrics["current_month_sales"]
    change = metrics["mom_change_pct"]

    direction = "increased" if change >= 0 else "decreased"

    report = {
        "title": f"{region} Month-over-Month Sales Review",

        "context": (
            f"{region} sales were "
            f"₹{previous:,.2f} in the previous month "
            f"and ₹{current:,.2f} in the current month."
        ),

        "insight": (
            f"Sales {direction} by "
            f"{abs(change):.2f}% month over month."
        ),

        "implication": (
            f"The {abs(change):.2f}% change in {region} "
            f"sales should be reviewed against regional "
            f"and category-level performance before making "
            f"a business decision."
        ),

        "generated_at": datetime.now().isoformat()
    }

    return report


def save_report(report, path="/content/draft_report.json"):
    """
    Save the generated report as JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            indent=2
        )

    return path


if __name__ == "__main__":

    # Verified Guntur April → May metrics
    metrics = {
        "region": "Guntur",
        "previous_month_sales": 62442.27,
        "current_month_sales": 138738.93,
        "mom_change_pct": 122.19
    }

    report = draft_report_v1(metrics)

    print("=" * 60)
    print("PHARMEASY DRAFT REPORT")
    print("=" * 60)

    print("\nContext:")
    print(report["context"])

    print("\nInsight:")
    print(report["insight"])

    print("\nImplication:")
    print(report["implication"])

    path = save_report(report)

    print("\nSaved:", path)
