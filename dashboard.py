"""
SUCHNA AI — Premium AI-Powered Notice Board Platform
Streamlit dashboard entry point.
"""

import streamlit as st

_defaults = {
    "user": None,
    "current_page": "dashboard",
    "chat_history": [],
    "ocr_cache": "",
    "ai_preview": None,
    "confirm_delete_id": None,
    "global_search": "",
    "_last_nav_search": "",
}
for _key, _val in _defaults.items():
    if _key not in st.session_state:
        st.session_state[_key] = _val

st.set_page_config(
    page_title="SUCHNA AI | Never Miss What Matters",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config import BACKEND_URL
from api_client import (
    DB_FALLBACK_AVAILABLE,
    delete_notice_remote,
    fetch_notices,
    fetch_recommendations,
    is_backend_online,
    pin_notice_remote,
    unpin_notice_remote,
)
from ocr_utils import perform_ocr
from ui.constants import (
    PAGE_ASSISTANT,
    PAGE_DASHBOARD,
    PAGE_NOTICES,
    PAGE_PRIORITY,
    PAGE_RECOMMENDATIONS,
    PAGE_SETTINGS,
    PAGE_UPLOAD,
)
from ui.components import render_auth_page, render_sidebar, render_top_navbar
from ui.pages import (
    render_assistant_page,
    render_dashboard_page,
    render_notices_page,
    render_priority_page,
    render_recommendations_page,
    render_settings_page,
    render_upload_page,
)
from ui.styles import inject_styles
from ui.utils import compute_dashboard_stats

try:
    from db import add_notice, authenticate_user, register_user, get_notices
    from model import predict_category
    from engine import generate_summary, detect_deadlines
    from assistant import get_chatbot_response

    FALLBACK_AVAILABLE = DB_FALLBACK_AVAILABLE
except ImportError:
    FALLBACK_AVAILABLE = False
    authenticate_user = register_user = add_notice = get_notices = None
    predict_category = generate_summary = detect_deadlines = get_chatbot_response = None

if st.session_state.current_page == "dashboard":
    st.session_state.current_page = PAGE_DASHBOARD

API_ONLINE = is_backend_online()
logged_in = st.session_state.user is not None

if logged_in:
    render_sidebar(st.session_state.user)

inject_styles(logged_in=logged_in)

if not logged_in:
    render_auth_page(API_ONLINE, FALLBACK_AVAILABLE, authenticate_user, register_user)
    st.stop()

# ── Authenticated app ──
user = st.session_state.user

USER_ROLE = user["role"]
USER_BRANCH = user["branch"]
USER_YEAR = user["year"]


def load_all_notices(branch=None, year=None, category=None, priority=None, search=None):
    return fetch_notices(
        branch=branch,
        year=year,
        category=category,
        priority=priority,
        search=search,
        backend_url=BACKEND_URL,
        api_online=API_ONLINE,
    )


def pin_notice_action(notice_id):
    return pin_notice_remote(notice_id, backend_url=BACKEND_URL, api_online=API_ONLINE)


def unpin_notice_action(notice_id):
    return unpin_notice_remote(notice_id, backend_url=BACKEND_URL, api_online=API_ONLINE)


def delete_notice_action(notice_id):
    return delete_notice_remote(notice_id, backend_url=BACKEND_URL, api_online=API_ONLINE)


def fetch_recs(branch, year):
    return fetch_recommendations(branch, year, backend_url=BACKEND_URL, api_online=API_ONLINE)


stats_notices = load_all_notices(
    branch=USER_BRANCH if USER_ROLE == "student" else "All",
    year=USER_YEAR if USER_ROLE == "student" else "All",
)
upcoming = compute_dashboard_stats(stats_notices)["upcoming_deadlines"]

render_top_navbar(user, upcoming_count=upcoming)

if not API_ONLINE and not FALLBACK_AVAILABLE:
    st.error("Unable to load data. Please ensure the database is set up.")
    st.stop()

current_page = st.session_state.current_page

if current_page == PAGE_DASHBOARD:
    render_dashboard_page(load_all_notices, user)

elif current_page == PAGE_PRIORITY:
    render_priority_page(load_all_notices, user)

elif current_page == PAGE_NOTICES:
    render_notices_page(load_all_notices, user)

elif current_page == PAGE_UPLOAD:
    if USER_ROLE != "admin":
        st.warning("Admin access required.")
    else:
        render_upload_page(
            API_ONLINE,
            FALLBACK_AVAILABLE,
            load_all_notices,
            predict_category,
            generate_summary,
            detect_deadlines,
            add_notice,
            perform_ocr,
        )

elif current_page == PAGE_ASSISTANT:
    render_assistant_page(API_ONLINE, user, get_notices, get_chatbot_response)

elif current_page == PAGE_RECOMMENDATIONS:
    render_recommendations_page(fetch_recs, user)

elif current_page == PAGE_SETTINGS:
    render_settings_page(
        user,
        load_all_notices,
        pin_notice_action,
        unpin_notice_action,
        delete_notice_action,
    )

else:
    st.session_state.current_page = PAGE_DASHBOARD
    st.rerun()
