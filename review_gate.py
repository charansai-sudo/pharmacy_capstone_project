
import json
from datetime import datetime
from pathlib import Path


AUDIT_FILE = "/content/audit_log.jsonl"


def review_gate_v1(
    report,
    decision,
    run_id="run_001",
    region=None,
    reviewer_note=""
):
    """
    Human review gate.

    Allowed decisions:
        approve
        edit
        reject

    Only an approved report is allowed downstream.
    """

    allowed_decisions = {
        "approve",
        "edit",
        "reject"
    }

    decision = decision.lower().strip()

    if decision not in allowed_decisions:
        raise ValueError(
            f"Invalid decision: {decision}. "
            f"Use approve, edit, or reject."
        )

    if not isinstance(report, dict):
        raise TypeError(
            "report must be a dictionary"
        )

    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "run_id": run_id,
        "region": region or report.get("region", "Unknown"),
        "decision": decision,
        "reviewer_note": reviewer_note
    }

    with open(
        AUDIT_FILE,
        "a",
        encoding="utf-8"
    ) as f:
        f.write(
            json.dumps(audit_entry) + "\n"
        )

    if decision == "approve":
        return {
            "approved": True,
            "downstream_allowed": True,
            "report": report,
            "audit": audit_entry
        }

    return {
        "approved": False,
        "downstream_allowed": False,
        "report": report,
        "audit": audit_entry
    }


def read_audit_log(path=AUDIT_FILE):
    """
    Read all audit entries.
    """
    file_path = Path(path)

    if not file_path.exists():
        return []

    entries = []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        for line in f:
            line = line.strip()

            if line:
                entries.append(
                    json.loads(line)
                )

    return entries


if __name__ == "__main__":

    # Example report used for the human-review test
    report = {
        "region": "Guntur",
        "title": "Guntur Month-over-Month Sales Review",
        "context": (
            "Guntur sales were ₹62,442.27 in April "
            "and ₹138,738.93 in May."
        ),
        "insight": (
            "Sales increased by 122.19% month over month."
        ),
        "implication": (
            "The change should be reviewed before "
            "making a business decision."
        )
    }

    print("=" * 60)
    print("PHARMEASY REVIEW GATE")
    print("=" * 60)

    # Test 1: Approve
    approved = review_gate_v1(
        report=report,
        decision="approve",
        run_id="run_001",
        region="Guntur",
        reviewer_note="Metrics verified."
    )

    print("\nApprove test:")
    print("Approved:", approved["approved"])
    print(
        "Downstream allowed:",
        approved["downstream_allowed"]
    )

    # Test 2: Edit
    edited = review_gate_v1(
        report=report,
        decision="edit",
        run_id="run_002",
        region="Guntur",
        reviewer_note="Clarify implication."
    )

    print("\nEdit test:")
    print("Approved:", edited["approved"])
    print(
        "Downstream allowed:",
        edited["downstream_allowed"]
    )

    # Test 3: Reject
    rejected = review_gate_v1(
        report=report,
        decision="reject",
        run_id="run_003",
        region="Guntur",
        reviewer_note="Insufficient supporting evidence."
    )

    print("\nReject test:")
    print("Approved:", rejected["approved"])
    print(
        "Downstream allowed:",
        rejected["downstream_allowed"]
    )

    print("\nAudit log entries:")
    for entry in read_audit_log():
        print(entry)

    print("\nAudit log:", AUDIT_FILE)
