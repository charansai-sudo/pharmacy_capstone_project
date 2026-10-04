
import json
from pathlib import Path


STATE_FILE = "/content/metrics_state.json"


def calculate_mom_change(previous, current):
    """
    Calculate month-over-month percentage change.
    """
    if previous == 0:
        return None

    return ((current - previous) / previous) * 100


def flag_significant_regions_v1(changes, threshold=8):
    """
    Flag regions whose absolute MoM change is greater
    than the specified threshold.
    """
    return {
        region: abs(change) > threshold
        for region, change in changes.items()
    }


def get_significant_regions(changes, threshold=8):
    """
    Return only regions with significant changes.
    """
    flags = flag_significant_regions_v1(
        changes,
        threshold
    )

    return [
        region
        for region, flagged in flags.items()
        if flagged
    ]


def save_metrics_state(state, path=STATE_FILE):
    """
    Persist calculated metrics state as JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            state,
            f,
            indent=2
        )

    return path


def load_metrics_state(path=STATE_FILE):
    """
    Load previously saved metrics state.
    """
    file_path = Path(path)

    if not file_path.exists():
        return {}

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def update_metrics_state(
    changes,
    threshold=8,
    previous_state=None
):
    """
    Calculate flags and persist the latest metrics state.
    """
    flags = flag_significant_regions_v1(
        changes,
        threshold
    )

    state = {
        "threshold": threshold,
        "changes": changes,
        "flags": flags,
        "significant_regions": [
            region
            for region, flagged in flags.items()
            if flagged
        ]
    }

    if previous_state:
        state["previous_state"] = previous_state

    save_metrics_state(state)

    return state


if __name__ == "__main__":

    # Known Part 2 validation values
    april_to_may = {
        "Hyderabad": 13.91,
        "Warangal": -22.03,
        "Vijayawada": -3.81,
        "Visakhapatnam": -62.47,
        "Guntur": 122.19,
        "Tirupati": 66.87,
        "Karimnagar": 23.63,
        "Bengaluru": -16.29,
        "Nellore": 6.49
    }

    may_to_june = {
        "Hyderabad": 23.61,
        "Warangal": -14.84,
        "Vijayawada": -6.43,
        "Visakhapatnam": 99.11,
        "Guntur": -28.08,
        "Tirupati": -17.07,
        "Karimnagar": -44.00,
        "Bengaluru": 0.66,
        "Nellore": 3.52
    }

    print("=" * 60)
    print("PHARMEASY METRICS ENGINE")
    print("=" * 60)

    print("\nApril → May significant regions:")
    april_may_flags = flag_significant_regions_v1(
        april_to_may
    )

    print([
        region
        for region, flagged in april_may_flags.items()
        if flagged
    ])

    print("\nMay → June significant regions:")
    may_june_flags = flag_significant_regions_v1(
        may_to_june
    )

    print([
        region
        for region, flagged in may_june_flags.items()
        if flagged
    ])

    # Persist latest state
    state = update_metrics_state(
        may_to_june,
        threshold=8
    )

    print("\nState saved to:", STATE_FILE)
    print(
        "Significant regions:",
        state["significant_regions"]
    )
