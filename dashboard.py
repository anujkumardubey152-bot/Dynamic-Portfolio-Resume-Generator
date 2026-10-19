from collections import Counter
from datetime import date, datetime


ACTIVE_STATUSES = {
    "Interested",
    "Applied",
    "Assessment",
    "Interview",
    "Offer",
}


def _parse_date(value):
    """Parse a date in YYYY-MM-DD format; return None if invalid."""
    if not value:
        return None

    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def build_dashboard_data(applications, today=None):
    """
    Summarize application tracker records for a dashboard.

    applications should be a list of dictionaries returned by
    src.application_tracker.list_applications().
    """
    today = today or date.today()
    applications = list(applications or [])

    status_counts = Counter()
    upcoming_followups = []
    recent_applications = []
    active_count = 0
    overdue_count = 0

    for app in applications:
        status = str(app.get("status") or "Interested")
        status_counts[status] += 1

        if status in ACTIVE_STATUSES:
            active_count += 1

        followup = _parse_date(app.get("follow_up_date"))
        if (
            followup is not None
            and followup >= today
            and status not in {"Rejected", "Withdrawn"}
        ):
            upcoming_followups.append({
                **app,
                "_followup_date": followup,
            })

        if (
            followup is not None
            and followup < today
            and status not in {"Rejected", "Withdrawn", "Offer"}
        ):
            overdue_count += 1

        recent_applications.append(app)

    upcoming_followups.sort(key=lambda item: item["_followup_date"])

    def date_sort_key(app):
        value = (
            app.get("applied_date")
            or app.get("created_at")
            or ""
        )
        return str(value)

    recent_applications.sort(key=date_sort_key, reverse=True)

    return {
        "total_applications": len(applications),
        "active_applications": active_count,
        "interviews": status_counts.get("Interview", 0),
        "offers": status_counts.get("Offer", 0),
        "overdue_followups": overdue_count,
        "status_counts": dict(status_counts),
        "upcoming_followups": upcoming_followups[:10],
        "recent_applications": recent_applications[:10],
    }
