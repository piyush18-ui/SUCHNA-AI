"""Shared utility helpers for notice display and stats."""

import html
from datetime import datetime

from api_client import normalize_search_query


def esc(text):
    """Escape HTML in user-generated notice content."""
    return html.escape(str(text or ""))


def format_created_date(value):
    """Formats a database timestamp for display on notice cards."""
    if not value:
        return "N/A"
    try:
        if isinstance(value, str) and "T" in value:
            return datetime.fromisoformat(value.replace("Z", "")).strftime("%d %b %Y, %H:%M")
        if isinstance(value, str):
            return datetime.strptime(value[:19], "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y, %H:%M")
    except (ValueError, TypeError):
        pass
    return str(value)


def parse_deadline_date(date_str):
    """Parses common deadline formats returned by the AI engine."""
    if not date_str:
        return None
    cleaned = date_str.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    return None


def count_upcoming_deadlines(notices):
    """Counts notices with at least one deadline on or after today."""
    today = datetime.now().date()
    upcoming = 0
    for notice in notices:
        raw = notice.get("deadlines")
        if not raw:
            continue
        for part in raw.split(","):
            deadline = parse_deadline_date(part)
            if deadline and deadline >= today:
                upcoming += 1
                break
    return upcoming


def is_notice_pinned(notice):
    """Returns True when a notice is pinned."""
    return bool(notice.get("is_pinned", 0))


def count_ai_processed(notices):
    """Counts notices that have an AI-generated summary."""
    return sum(1 for n in notices if (n.get("summary") or "").strip())


def compute_dashboard_stats(notices):
    """Builds summary metrics for the dashboard stat cards."""
    return {
        "total": len(notices),
        "pinned": sum(1 for n in notices if is_notice_pinned(n)),
        "upcoming_deadlines": count_upcoming_deadlines(notices),
        "ai_processed": count_ai_processed(notices),
    }


def notice_matches_search(notice, query):
    """Returns True when a notice matches a search query."""
    normalized = normalize_search_query(query)
    if not normalized:
        return True
    needle = normalized.lower()
    fields = (
        notice.get("title", ""),
        notice.get("content", ""),
        notice.get("category", ""),
        notice.get("summary", ""),
    )
    return any(needle in (field or "").lower() for field in fields)


def get_search_match_labels(notice, query):
    """Returns which fields matched the current search query."""
    normalized = normalize_search_query(query)
    if not normalized:
        return []
    needle = normalized.lower()
    labels = []
    if needle in (notice.get("title") or "").lower():
        labels.append("Title")
    if needle in (notice.get("content") or "").lower():
        labels.append("Content")
    if needle in (notice.get("category") or "").lower():
        labels.append("Category")
    if needle in (notice.get("summary") or "").lower():
        labels.append("Summary")
    return labels


def filter_admin_notices(notices, search="", category="All", priority="All", pin_filter="All"):
    """Filters notices for the admin management panel."""
    filtered = list(notices)

    if category and category != "All":
        filtered = [n for n in filtered if n.get("category") == category]
    if priority and priority != "All":
        filtered = [n for n in filtered if n.get("priority") == priority]
    if pin_filter == "Pinned Only":
        filtered = [n for n in filtered if is_notice_pinned(n)]
    elif pin_filter == "Unpinned Only":
        filtered = [n for n in filtered if not is_notice_pinned(n)]
    if search:
        filtered = [n for n in filtered if notice_matches_search(n, search)]

    filtered.sort(
        key=lambda n: (1 if is_notice_pinned(n) else 0, n.get("created_at") or ""),
        reverse=True,
    )
    return filtered
