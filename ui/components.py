"""Reusable UI components: auth, sidebar, navbar, cards."""

import os

import requests
import streamlit as st

from api_client import normalize_search_query
from config import BACKEND_URL
from ui.constants import (
    ADMIN_ONLY_PAGES,
    BRAND_EMOJI,
    BRAND_NAME,
    FEATURE_BADGES,
    NAV_ITEMS,
    PAGE_ASSISTANT,
    PAGE_DASHBOARD,
    PAGE_NOTICES,
    PAGE_PRIORITY,
    SUBHEADING,
    TAGLINE,
)
from ui.utils import (
    esc,
    format_created_date,
    get_search_match_labels,
    is_notice_pinned,
)


def sign_out():
    """Clear session and return to auth screen."""
    st.session_state.user = None
    st.session_state.chat_history = []
    st.session_state.ocr_cache = ""
    st.session_state.ai_preview = None
    st.session_state.current_page = PAGE_DASHBOARD
    st.rerun()


def render_auth_page(api_online, fallback_available, authenticate_user, register_user):
    """Premium centered authentication experience."""
    if not api_online and not fallback_available:
        st.error("Unable to connect. Please ensure the database is set up and try again.")
        st.stop()

    badges_html = "".join(
        f'<span class="feature-badge">{esc(b)}</span>' for b in FEATURE_BADGES
    )

    st.markdown(f"""
     <div class="auth-hero">
    <div class="auth-brand">{BRAND_EMOJI} {esc(BRAND_NAME)}</div>
    <div class="auth-tagline">{esc(TAGLINE)}</div>
    <div class="auth-sub">{esc(SUBHEADING)}</div>
    <div class="feature-badges">{badges_html}</div>
</div>
""", unsafe_allow_html=True)
    

    
    auth_action = st.radio(
        "Action",
        ["Sign In", "Create Account"],
        horizontal=True,
        label_visibility="collapsed",
    )

    login_username = st.text_input("Username", key="auth_user", placeholder="Enter username")
    login_password = st.text_input("Password", type="password", key="auth_pass", placeholder="Enter password")

    reg_role = "student"
    reg_branch = "All"
    reg_year = "All"
    reg_email = ""
    if auth_action == "Create Account":
        reg_role = st.selectbox("Role", ["student", "admin"])
        if reg_role == "student":
            reg_branch = st.selectbox(
                "Branch",
                ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil"],
            )
            reg_year = st.selectbox("Current Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        else:
            reg_email = st.text_input(
                "Institutional Email",
                placeholder="admin@college.edu",
                key="auth_admin_email",
            )
            st.caption("Admin accounts require an authorized institutional email.")

    if st.button("Continue →", type="primary", use_container_width=True):
        if not login_username or not login_password:
            st.warning("Please fill in all fields.")
        elif auth_action == "Create Account" and reg_role == "admin" and not reg_email:
            st.error("Admin registration requires a valid institutional email.")
        elif auth_action == "Sign In":
            _handle_login(login_username, login_password, api_online, authenticate_user)
        else:
            _handle_register(
                login_username, login_password, reg_role, reg_branch, reg_year,
                reg_email, api_online, register_user,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def _handle_login(username, password, api_online, authenticate_user):
    if api_online:
        try:
            res = requests.post(
                f"{BACKEND_URL}/api/auth/login",
                json={"username": username, "password": password},
            )
            payload = res.json()
            if payload.get("success"):
                st.session_state.user = payload["user"]
                st.session_state.current_page = PAGE_DASHBOARD
                st.rerun()
            else:
                st.error(payload.get("message", "Login failed."))
        except Exception as exc:
            st.error(f"Network error: {exc}")
    else:
        result = authenticate_user(username, password)
        if result["success"]:
            st.session_state.user = result["user"]
            st.session_state.current_page = PAGE_DASHBOARD
            st.rerun()
        else:
            st.error(result["message"])


def _handle_register(username, password, role, branch, year, email, api_online, register_user):
    if api_online:
        try:
            register_payload = {
                "username": username,
                "password": password,
                "role": role,
                "branch": branch,
                "year": year,
            }
            if role == "admin":
                register_payload["email"] = email
            res = requests.post(f"{BACKEND_URL}/api/auth/register", json=register_payload)
            payload = res.json()
            if payload.get("success"):
                st.success("Account created! Please sign in.")
            else:
                st.error(payload.get("message", "Registration failed."))
        except Exception as exc:
            st.error(f"Network error: {exc}")
    else:
        result = register_user(
            username, password, role, branch, year,
            email=email if role == "admin" else None,
        )
        if result["success"]:
            st.success("Account created! Please sign in.")
        else:
            st.error(result["message"])


def _user_initial(username):
    return esc(username[0].upper()) if username else "?"


def render_sidebar(user):
    """Premium sidebar with navigation and profile card."""
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-brand">
            <p class="sidebar-brand-title">{BRAND_EMOJI} {esc(BRAND_NAME)}</p>
            <p class="sidebar-brand-tag">{esc(TAGLINE)}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="nav-label">Navigation</p>', unsafe_allow_html=True)

        is_admin = user["role"] == "admin"
        nav_options = []
        nav_labels = []
        for page_id, label in NAV_ITEMS:
            if page_id in ADMIN_ONLY_PAGES and not is_admin:
                continue
            nav_options.append(page_id)
            nav_labels.append(label)

        current = st.session_state.get("current_page", PAGE_DASHBOARD)
        if current not in nav_options:
            current = nav_options[0]

        selected_label = st.radio(
            "Navigation",
            nav_labels,
            index=nav_options.index(current),
            label_visibility="collapsed",
        )
        selected_page = nav_options[nav_labels.index(selected_label)]
        if selected_page != st.session_state.get("current_page"):
            st.session_state.current_page = selected_page
            st.rerun()

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="nav-label">Account</p>', unsafe_allow_html=True)
        role_display = user["role"].title()
        initial = _user_initial(user["username"])
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-avatar">{initial}</div>
            <div class="profile-info">
                <p class="profile-name">{esc(user['username'])}</p>
                <p class="profile-role">{esc(role_display)}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Sign Out", use_container_width=True, key="sidebar_signout"):
            sign_out()


def render_top_navbar(user, upcoming_count=0):
    """Premium top navbar with search, notifications, and user menu."""
    st.markdown('<div class="top-nav-shell">', unsafe_allow_html=True)
    c_search, c_notif, c_user = st.columns([5.5, 0.6, 1.4])

    with c_search:
        global_search = st.text_input(
            "Search",
            placeholder="🔍  Search notices, categories, summaries...",
            key="navbar_search",
            label_visibility="collapsed",
            value=st.session_state.get("global_search", ""),
        )
        if global_search and global_search != st.session_state.get("_last_nav_search"):
            st.session_state.global_search = global_search
            st.session_state._last_nav_search = global_search
            if st.session_state.get("current_page") != PAGE_NOTICES:
                st.session_state.current_page = PAGE_NOTICES
                st.rerun()

    with c_notif:
        badge = (
            f'<span class="notif-badge">{upcoming_count}</span>'
            if upcoming_count > 0 else ""
        )
        st.markdown(
            f'<div class="nav-icon-btn" title="{upcoming_count} upcoming deadlines">'
            f'🔔{badge}</div>',
            unsafe_allow_html=True,
        )

    with c_user:
        initial = _user_initial(user["username"])
        with st.popover(f"👤  {user['username'][:14]}"):
            st.markdown(f"""
            <div class="nav-user-chip" style="margin-bottom:0.75rem;border:none;background:transparent;padding:0;">
                <div class="nav-user-avatar">{initial}</div>
                <div>
                    <div style="font-weight:700;font-size:0.95rem;">{esc(user['username'])}</div>
                    <div style="font-size:0.78rem;color:var(--text-muted);">{user['role'].title()}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if user.get("branch") and user["role"] == "student":
                st.caption(f"{user.get('branch', '')} · {user.get('year', '')}")
            if st.button("Sign Out", key="nav_signout", use_container_width=True):
                sign_out()

    st.markdown("</div>", unsafe_allow_html=True)


def render_welcome_hero(username):
    """Dashboard welcome hero with gradient and feature pills."""
    features_html = "".join(
        f'<span class="welcome-feature">{esc(b)}</span>' for b in FEATURE_BADGES
    )
    st.markdown(f"""
    <div class="welcome-hero">
        <p class="welcome-greeting">Welcome Back 👋</p>
        <h1 class="welcome-title">{BRAND_EMOJI} {esc(BRAND_NAME)}</h1>
        <p class="welcome-tagline">{esc(TAGLINE)}</p>
        <p class="welcome-subtitle">{esc(SUBHEADING)}</p>
        <div class="welcome-features">{features_html}</div>
    </div>
    """, unsafe_allow_html=True)


def render_page_header(title, subtitle):
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{esc(title)}</h1>
        <p class="page-subtitle">{esc(subtitle)}</p>
    </div>
    """, unsafe_allow_html=True)


def render_stat_cards(stats):
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card stat-card-1">
            <div class="stat-icon">📄</div>
            <div class="stat-label">Total Notices</div>
            <div class="stat-value">{stats['total']}</div>
        </div>
        <div class="stat-card stat-card-2">
            <div class="stat-icon">📌</div>
            <div class="stat-label">Priority Notices</div>
            <div class="stat-value">{stats['pinned']}</div>
        </div>
        <div class="stat-card stat-card-3">
            <div class="stat-icon">⏰</div>
            <div class="stat-label">Upcoming Deadlines</div>
            <div class="stat-value">{stats['upcoming_deadlines']}</div>
        </div>
        <div class="stat-card stat-card-4">
            <div class="stat-icon">🤖</div>
            <div class="stat-label">AI Processed</div>
            <div class="stat-value">{stats['ai_processed']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_search_results_bar(result_count, total_count, search_query, category, priority, pin_filter=None):
    active_filters = []
    if normalize_search_query(search_query):
        active_filters.append(f'query "<b>{esc(search_query.strip())}</b>"')
    if category and category != "All":
        active_filters.append(f"category <b>{esc(category)}</b>")
    if priority and priority != "All":
        active_filters.append(f"priority <b>{esc(priority)}</b>")
    if pin_filter and pin_filter != "All":
        active_filters.append(f"status <b>{esc(pin_filter)}</b>")

    filter_text = f" · Filters: {', '.join(active_filters)}" if active_filters else ""
    st.markdown(
        f'<div class="search-results-bar">Found <b>{result_count}</b> of <b>{total_count}</b> notices{filter_text}</div>',
        unsafe_allow_html=True,
    )


def render_search_panel(key_prefix="main", show_pin_filter=False, default_search=""):
    st.markdown("""
    <div class="search-panel">
        <div class="search-panel-title">🔍 Search & Filter</div>
        <p class="search-hint">Search across titles, content, categories, and AI summaries.</p>
        <div class="search-scope-tags">
            <span class="search-scope-tag">Title</span>
            <span class="search-scope-tag">Content</span>
            <span class="search-scope-tag">Category</span>
            <span class="search-scope-tag">Summary</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    search_key = f"{key_prefix}_search"
    category_key = f"{key_prefix}_category"
    priority_key = f"{key_prefix}_priority"
    pin_key = f"{key_prefix}_pin"

    if default_search and search_key not in st.session_state:
        st.session_state[search_key] = default_search

    if show_pin_filter:
        col_search, col_cat, col_prio, col_pin, col_clear = st.columns([2.4, 1, 1, 1, 0.6])
    else:
        col_search, col_cat, col_prio, col_clear = st.columns([2.6, 1, 1, 0.7])

    with col_search:
        search_query = st.text_input(
            "Search notices",
            placeholder="Try: exam, placement, workshop...",
            key=search_key,
            label_visibility="collapsed",
        )
    with col_cat:
        category = st.selectbox(
            "Category",
            ["All", "Exams", "Placements", "Events", "Assignments", "Workshops", "General"],
            key=category_key,
            label_visibility="collapsed",
        )
    with col_prio:
        priority = st.selectbox(
            "Priority",
            ["All", "High", "Medium", "Low"],
            key=priority_key,
            label_visibility="collapsed",
        )

    pin_filter = None
    if show_pin_filter:
        with col_pin:
            pin_filter = st.selectbox(
                "Pin status",
                ["All", "Pinned Only", "Unpinned Only"],
                key=pin_key,
                label_visibility="collapsed",
            )
        with col_clear:
            if st.button("✕", key=f"{key_prefix}_clear", help="Clear filters"):
                for state_key in (search_key, category_key, priority_key, pin_key):
                    st.session_state.pop(state_key, None)
                st.rerun()
    else:
        with col_clear:
            if st.button("✕", key=f"{key_prefix}_clear", help="Clear filters"):
                for state_key in (search_key, category_key, priority_key):
                    st.session_state.pop(state_key, None)
                st.session_state.pop("global_search", None)
                st.rerun()

    return search_query, category, priority, pin_filter


def _notice_card_html(notice, variant="glass", search_query=None, show_pin_badge=False):
    category = notice.get("category", "General")
    badge_class = f"badge-{category.lower()}"
    priority = notice.get("priority", "Medium")
    priority_badge_class = f"priority-badge-{priority.lower()}"
    pin_html = '<span class="pin-badge">🔥 PINNED</span>' if show_pin_badge else ""
    created_at = format_created_date(notice.get("created_at"))
    deadline_text = notice.get("deadlines") or "No deadline"
    summary_text = notice.get("summary") or notice.get("content", "")
    if len(summary_text) > 180:
        summary_text = summary_text[:180] + "..."
    match_labels = get_search_match_labels(notice, search_query)
    match_html = "".join(f'<span class="match-badge">{esc(label)}</span>' for label in match_labels)

    extra_class = ""
    if variant == "priority":
        card_class = "priority-zone-card"
        if show_pin_badge:
            extra_class += " pinned-card"
        if priority == "High":
            extra_class += " high-priority"
    else:
        card_class = "glass-card"

    return f"""
    <div class="{card_class}{extra_class}">
        <div class="notice-card-header">
            <div class="notice-meta-row">
                {pin_html}
                <span class="badge {badge_class}">{esc(category)}</span>
                <span class="priority-badge {priority_badge_class}">{esc(priority)}</span>
                {match_html}
            </div>
        </div>
        <h3 class="notice-title">{esc(notice.get('title', 'Untitled'))}</h3>
        <p class="notice-summary">{esc(summary_text)}</p>
        <div class="notice-footer">
            <span>⏰ {esc(deadline_text)}</span>
            <span>📅 {esc(created_at)}</span>
        </div>
    </div>
    """


def render_notice_card(notice, variant="glass", search_query=None, key_prefix="notice"):
    """Render a notice card with expandable details."""
    pinned = is_notice_pinned(notice)
    st.markdown(
        _notice_card_html(notice, variant=variant, search_query=search_query, show_pin_badge=pinned),
        unsafe_allow_html=True,
    )
    notice_id = notice.get("id", key_prefix)
    with st.expander("View Details"):
        st.markdown(f"**Summary:** {notice.get('summary') or 'No summary generated.'}")
        content = notice.get("content", "")
        st.caption(content[:600] + ("..." if len(content) > 600 else ""))
        if notice.get("deadlines"):
            st.markdown(f"**Deadlines:** {notice['deadlines']}")
        if notice.get("file_path"):
            st.markdown(f"**Attachment:** `{os.path.basename(notice['file_path'])}`")


def render_notice_grid(notices, search_query=None, key_prefix="grid"):
    """Responsive notice card grid."""
    if not notices:
        return
    cols_per_row = 3
    for i in range(0, len(notices), cols_per_row):
        row = notices[i:i + cols_per_row]
        cols = st.columns(len(row))
        for col, notice in zip(cols, row):
            with col:
                render_notice_card(
                    notice,
                    variant="glass",
                    search_query=search_query,
                    key_prefix=f"{key_prefix}_{notice.get('id', i)}",
                )


def render_priority_notice(notice, search_query=None):
    """Prominent priority zone card."""
    st.markdown(
        _notice_card_html(notice, variant="priority", search_query=search_query, show_pin_badge=True),
        unsafe_allow_html=True,
    )
    notice_id = notice.get("id", "prio")
    with st.expander("View Details"):
        st.markdown(f"**Summary:** {notice.get('summary') or 'N/A'}")
        st.markdown(f"**Content:** {notice.get('content', '')[:500]}")
        if notice.get("deadlines"):
            st.markdown(f"**Deadlines:** {notice['deadlines']}")


def render_admin_manage_card(notice, search_query, pin_action, unpin_action, delete_action):
    """Admin notice management card with premium actions."""
    notice_id = notice["id"]
    pinned = is_notice_pinned(notice)
    category = notice.get("category", "General")
    badge_class = f"badge-{category.lower()}"
    priority = notice.get("priority", "Medium")
    priority_badge_class = f"priority-badge-{priority.lower()}"
    card_class = "admin-manage-card pinned" if pinned else "admin-manage-card"
    pin_html = '<span class="pin-badge">🔥 PINNED</span>' if pinned else ""
    match_labels = get_search_match_labels(notice, search_query)
    match_html = "".join(f'<span class="match-badge">{esc(label)}</span>' for label in match_labels)
    summary = notice.get("summary") or notice.get("content", "")
    deadline_text = notice.get("deadlines") or "No deadline"
    created_at = format_created_date(notice.get("created_at"))

    st.markdown(f"""
    <div class="{card_class}">
        <div class="notice-meta-row">
            {pin_html}
            <span class="badge {badge_class}">{esc(category)}</span>
            <span class="priority-badge {priority_badge_class}">{esc(priority)}</span>
            {match_html}
        </div>
        <h4 class="admin-manage-title">{esc(notice.get('title', 'Untitled'))}</h4>
        <p class="admin-manage-summary">{esc(summary[:220])}{'...' if len(summary) > 220 else ''}</p>
        <div class="admin-manage-meta">
            <span><b>Branch:</b> {esc(notice.get('branch', 'All'))}</span>
            <span><b>Year:</b> {esc(notice.get('year', 'All'))}</span>
            <span><b>Deadline:</b> {esc(deadline_text)}</span>
            <span><b>Posted:</b> {esc(created_at)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_pin, col_del, _ = st.columns([1.2, 1.2, 3.6])
    with col_pin:
        if pinned:
            if st.button("📍 Unpin", key=f"admin_unpin_{notice_id}", use_container_width=True):
                result = unpin_action(notice_id)
                if result.get("success"):
                    st.toast("Notice unpinned.", icon="📍")
                    st.rerun()
                else:
                    st.error(result.get("message", "Failed to unpin."))
        else:
            if st.button("📌 Pin", key=f"admin_pin_{notice_id}", use_container_width=True):
                result = pin_action(notice_id)
                if result.get("success"):
                    st.toast("Pinned to Priority Zone.", icon="🔥")
                    st.rerun()
                else:
                    st.error(result.get("message", "Failed to pin."))

    with col_del:
        if st.session_state.confirm_delete_id != notice_id:
            if st.button("🗑️ Delete", key=f"admin_del_{notice_id}", use_container_width=True):
                st.session_state.confirm_delete_id = notice_id
                st.rerun()
        else:
            if st.button("✅ Confirm", key=f"admin_confirm_{notice_id}", use_container_width=True):
                result = delete_action(notice_id)
                st.session_state.confirm_delete_id = None
                if result.get("success"):
                    st.toast("Notice deleted.", icon="🗑️")
                    st.rerun()
                else:
                    st.error(result.get("message", "Failed to delete."))

    if st.session_state.confirm_delete_id == notice_id:
        st.warning(f"Delete **{notice.get('title')}**? Click Confirm or cancel.")
        if st.button("Cancel", key=f"admin_cancel_{notice_id}"):
            st.session_state.confirm_delete_id = None
            st.rerun()

    with st.expander("Full details"):
        st.markdown(f"**Summary:** {notice.get('summary') or 'N/A'}")
        st.markdown(f"**Content:** {notice.get('content', '')}")
        if notice.get("file_path"):
            st.markdown(f"**Attachment:** `{os.path.basename(notice['file_path'])}`")
