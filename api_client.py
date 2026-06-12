"""
HTTP client helpers for the Streamlit dashboard.
Falls back to local database modules when the REST API is offline.
"""

import requests

from config import BACKEND_URL

try:
    from db import (
        get_notices,
        delete_notice,
        pin_notice,
        unpin_notice,
        normalize_search_query,
    )
    from services import build_recommendations

    DB_FALLBACK_AVAILABLE = True
except ImportError:
    DB_FALLBACK_AVAILABLE = False

    def normalize_search_query(search_query):
        if not search_query or not isinstance(search_query, str):
            return None
        cleaned = search_query.strip()
        return cleaned if cleaned else None


def is_backend_online(backend_url=BACKEND_URL):
    """Returns True when the Flask REST API responds successfully."""
    try:
        response = requests.get(f"{backend_url.rstrip('/')}/api/notices", timeout=1.0)
        return response.status_code == 200
    except requests.RequestException:
        return False


def _api_request(method, path, backend_url=BACKEND_URL, **kwargs):
    """Performs an HTTP request against the noticeboard API."""
    url = f"{backend_url.rstrip('/')}{path}"
    response = requests.request(method, url, **kwargs)
    return response.json()


def fetch_notices(branch=None, year=None, category=None, priority=None, search=None,
                  backend_url=BACKEND_URL, api_online=None):
    """Loads notices from the API, or from SQLite when offline."""
    search = normalize_search_query(search)

    if api_online is None:
        api_online = is_backend_online(backend_url)

    if api_online:
        try:
            params = {}
            if branch and branch != "All":
                params["branch"] = branch
            if year and year != "All":
                params["year"] = year
            if category and category != "All":
                params["category"] = category
            if priority and priority != "All":
                params["priority"] = priority
            if search:
                params["search"] = search
            payload = _api_request("GET", "/api/notices", backend_url=backend_url, params=params)
            return payload.get("notices", [])
        except (requests.RequestException, ValueError):
            pass

    if DB_FALLBACK_AVAILABLE:
        return get_notices(branch, year, category, priority, search)
    return []


def pin_notice_remote(notice_id, backend_url=BACKEND_URL, api_online=None):
    if api_online is None:
        api_online = is_backend_online(backend_url)
    if api_online:
        try:
            return _api_request("POST", f"/api/notices/{notice_id}/pin", backend_url=backend_url)
        except (requests.RequestException, ValueError) as exc:
            return {"success": False, "message": str(exc)}
    if DB_FALLBACK_AVAILABLE:
        return pin_notice(notice_id)
    return {"success": False, "message": "No backend or local database available."}


def unpin_notice_remote(notice_id, backend_url=BACKEND_URL, api_online=None):
    if api_online is None:
        api_online = is_backend_online(backend_url)
    if api_online:
        try:
            return _api_request("POST", f"/api/notices/{notice_id}/unpin", backend_url=backend_url)
        except (requests.RequestException, ValueError) as exc:
            return {"success": False, "message": str(exc)}
    if DB_FALLBACK_AVAILABLE:
        return unpin_notice(notice_id)
    return {"success": False, "message": "No backend or local database available."}


def delete_notice_remote(notice_id, backend_url=BACKEND_URL, api_online=None):
    if api_online is None:
        api_online = is_backend_online(backend_url)
    if api_online:
        try:
            return _api_request("DELETE", f"/api/notices/{notice_id}", backend_url=backend_url)
        except (requests.RequestException, ValueError) as exc:
            return {"success": False, "message": str(exc)}
    if DB_FALLBACK_AVAILABLE:
        return delete_notice(notice_id)
    return {"success": False, "message": "No backend or local database available."}


def fetch_recommendations(branch, year, backend_url=BACKEND_URL, api_online=None):
    if api_online is None:
        api_online = is_backend_online(backend_url)
    if api_online:
        try:
            payload = _api_request(
                "GET",
                "/api/recommendations",
                backend_url=backend_url,
                params={"branch": branch, "year": year},
            )
            return payload.get("notices", [])
        except (requests.RequestException, ValueError):
            pass

    if DB_FALLBACK_AVAILABLE:
        notices = get_notices(branch=branch, year=year)
        return build_recommendations(notices, branch=branch, year=year)
    return []
