"""Page-level views for SUCHNA AI dashboard."""

import os

import requests
import streamlit as st

from config import BACKEND_URL
from ocr_utils import perform_ocr
from ui.components import (
    render_admin_manage_card,
    render_notice_grid,
    render_page_header,
    render_priority_notice,
    render_search_panel,
    render_search_results_bar,
    render_stat_cards,
    render_welcome_hero,
)
from ui.constants import PAGE_NOTICES, PAGE_PRIORITY, SUGGESTED_PROMPTS
from ui.utils import (
    compute_dashboard_stats,
    esc,
    filter_admin_notices,
    is_notice_pinned,
)


def _scope_notices(load_all_notices, user_role, user_branch, user_year, **filters):
    if user_role == "student":
        return load_all_notices(branch=user_branch, year=user_year, **filters)
    return load_all_notices(branch="All", year="All", **filters)


def _scope_stats_notices(load_all_notices, user_role, user_branch, user_year):
    return _scope_notices(load_all_notices, user_role, user_branch, user_year)


def render_dashboard_page(load_all_notices, user):
    """Home dashboard with hero, stats, and priority preview."""
    render_welcome_hero(user["username"])

    stats_notices = _scope_stats_notices(
        load_all_notices, user["role"], user["branch"], user["year"],
    )
    render_stat_cards(compute_dashboard_stats(stats_notices))

    notices = _scope_notices(load_all_notices, user["role"], user["branch"], user["year"])
    pinned = [n for n in notices if is_notice_pinned(n)]
    high_priority = [n for n in notices if n.get("priority") == "High" and not is_notice_pinned(n)]

    preview = (pinned + high_priority)[:3]
    if preview:
        st.markdown(
            '<div class="section-header">'
            '<p class="section-title">🔥 Priority Zone Preview</p>'
            '<span class="section-badge">Important</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        for notice in preview:
            render_priority_notice(notice)

        if st.button("View All in Priority Zone →", key="goto_priority"):
            st.session_state.current_page = PAGE_PRIORITY
            st.rerun()

    recent = [n for n in notices if not is_notice_pinned(n)][:6]
    if recent:
        st.markdown(
            '<div class="section-header">'
            '<p class="section-title">📰 Recent Notices</p>'
            '<span class="section-badge">Latest</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        render_notice_grid(recent, key_prefix="dash_recent")

    if not notices:
        st.info("📭 No notices yet. Check back soon for campus updates.")


def render_priority_page(load_all_notices, user):
    """Dedicated Priority Zone for pinned and urgent notices."""
    render_page_header(
        "🔥 Priority Zone",
        "Your most important notices — pinned updates and high-priority alerts.",
    )

    notices = _scope_notices(load_all_notices, user["role"], user["branch"], user["year"])
    pinned = [n for n in notices if is_notice_pinned(n)]
    high_priority = [n for n in notices if n.get("priority") == "High" and not is_notice_pinned(n)]

    pinned.sort(key=lambda n: n.get("created_at") or "", reverse=True)
    high_priority.sort(key=lambda n: n.get("created_at") or "", reverse=True)

    if pinned:
        st.markdown('<p class="priority-section-title">📌 Pinned Notices</p>', unsafe_allow_html=True)
        for notice in pinned:
            render_priority_notice(notice)

    if high_priority:
        st.markdown('<p class="section-title">🚨 High Priority Alerts</p>', unsafe_allow_html=True)
        for notice in high_priority:
            render_priority_notice(notice)

    if not pinned and not high_priority:
        st.info("No priority notices right now. Important updates will appear here when pinned or marked high priority.")


def render_notices_page(load_all_notices, user):
    """Full notice grid with search and filters."""
    render_page_header(
        "📰 Notices",
        "Browse all AI-summarized notices with smart search and filters.",
    )

    default_search = st.session_state.get("global_search", "")
    if default_search:
        st.session_state["main_search"] = default_search
    search_query, category_filter, priority_filter, _ = render_search_panel(
        key_prefix="main",
        default_search=default_search,
    )

    if user["role"] == "student":
        notices = load_all_notices(
            branch=user["branch"], year=user["year"],
            category=category_filter, priority=priority_filter, search=search_query,
        )
        stats_notices = load_all_notices(branch=user["branch"], year=user["year"])
    else:
        notices = load_all_notices(
            branch="All", year="All",
            category=category_filter, priority=priority_filter, search=search_query,
        )
        stats_notices = load_all_notices(branch="All", year="All")

    render_search_results_bar(
        len(notices), len(stats_notices), search_query, category_filter, priority_filter,
    )

    regular = [n for n in notices if not is_notice_pinned(n)]
    pinned_in_results = [n for n in notices if is_notice_pinned(n)]

    if pinned_in_results:
        st.markdown('<p class="section-title">🔥 Also in Priority Zone</p>', unsafe_allow_html=True)
        render_notice_grid(pinned_in_results, search_query=search_query, key_prefix="notices_pinned")

    st.markdown('<p class="section-title">All Notices</p>', unsafe_allow_html=True)
    if not regular and not pinned_in_results:
        st.info("📭 No notices matched your search. Try different keywords or clear filters.")
    elif regular:
        render_notice_grid(regular, search_query=search_query, key_prefix="notices_all")


def render_assistant_page(api_online, user, get_notices_fn, get_chatbot_response):
    """Premium AI assistant chat panel."""
    render_page_header(
        "🤖 Ask Suchna AI",
        "Your intelligent campus assistant — ask about exams, placements, events, and deadlines.",
    )

    st.markdown('<div class="assistant-shell">', unsafe_allow_html=True)
    st.markdown("""
    <div class="assistant-header-bar">
        <p class="assistant-header-title">🤖 Suchna AI Assistant</p>
        <p class="assistant-header-sub">Powered by your notice board data</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="chat-empty-state">
            <div class="chat-empty-icon">✨</div>
            <p class="chat-empty-title">Hi! I'm Suchna AI</p>
            <p>Ask me anything about your campus notices, exams, or deadlines.</p>
        </div>
        """, unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(
                f'<div class="chat-bubble-user">'
                f'<div class="chat-bubble-label">You</div>{esc(chat["text"])}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-bubble-bot">'
                f'<div class="chat-bubble-label">Suchna AI</div>{esc(chat["text"])}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('<div class="prompts-section">', unsafe_allow_html=True)
    st.markdown('<p class="prompts-label">Suggested prompts</p>', unsafe_allow_html=True)
    prompt_cols = st.columns(len(SUGGESTED_PROMPTS))
    for col, prompt in zip(prompt_cols, SUGGESTED_PROMPTS):
        with col:
            if st.button(prompt, key=f"prompt_{prompt[:20]}", use_container_width=True):
                st.session_state.pending_chat_query = prompt
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    pending = st.session_state.pop("pending_chat_query", None)
    with st.form("chat_form", clear_on_submit=True):
        default_val = pending or ""
        chat_query = st.text_input(
            "Message",
            placeholder="Ask about exams, placements, deadlines...",
            value=default_val,
            label_visibility="collapsed",
        )
        submit_chat = st.form_submit_button("Send →", type="primary", use_container_width=True)

    if submit_chat and chat_query:
        st.session_state.chat_history.append({"role": "user", "text": chat_query})
        if api_online:
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/chatbot",
                    json={"query": chat_query, "branch": user["branch"], "year": user["year"]},
                )
                bot_reply = res.json().get("response", "Error fetching reply.")
            except Exception as exc:
                bot_reply = f"Error: {exc}"
        else:
            notices_list = get_notices_fn(branch=user["branch"], year=user["year"])
            bot_reply = get_chatbot_response(chat_query, notices_list)
        st.session_state.chat_history.append({"role": "bot", "text": bot_reply})
        st.rerun()


def render_recommendations_page(fetch_recommendations_fn, user):
    """Smart recommendation panel."""
    render_page_header(
        "🎯 Recommended For You",
        "Personalized notice suggestions based on your branch, year, and interests.",
    )

    if user["role"] == "admin":
        st.info("Recommendations are tailored for student profiles. Switch to a student account to preview.")
        return

    st.caption(f"Profile: {user['branch']} · {user['year']}")
    recs = fetch_recommendations_fn(user["branch"], user["year"])

    if not recs:
        st.info("📭 No recommendations available yet.")
        return

    top = recs[0]
    st.markdown(f"""
    <div class="rec-featured">
        <span class="rec-top-badge">⭐ TOP PICK · {esc(str(top.get('recommendation_score', 'N/A')))} pts</span>
        <h2>{esc(top['title'])}</h2>
        <p>{esc(top.get('summary', ''))}</p>
    </div>
    """, unsafe_allow_html=True)

    if len(recs) > 1:
        st.markdown(
            '<div class="section-header">'
            '<p class="section-title">More Recommendations</p>'
            '<span class="section-badge">For You</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        rec_cards_html = '<div class="rec-grid">'
        for rec in recs[1:6]:
            cat = rec.get("category", "General")
            rec_cards_html += f"""
            <div class="rec-card">
                <div class="notice-meta-row" style="margin-bottom:0.75rem;">
                    <span class="badge badge-{cat.lower()}">{esc(cat)}</span>
                    <span class="match-badge">{esc(str(rec.get('recommendation_score', 'N/A')))} pts</span>
                </div>
                <h3 class="notice-title">{esc(rec['title'])}</h3>
                <p class="notice-summary">{esc(rec.get('summary', ''))}</p>
            </div>
            """
        rec_cards_html += "</div>"
        st.markdown(rec_cards_html, unsafe_allow_html=True)


def render_upload_page(
    api_online,
    fallback_available,
    load_all_notices,
    predict_category,
    generate_summary,
    detect_deadlines,
    add_notice_fn,
    perform_ocr_fn,
):
    """Admin notice upload with OCR and AI pipeline."""
    render_page_header(
        "📤 Upload Notice",
        "Publish notices with AI-powered OCR, categorization, and deadline detection.",
    )

    st.markdown('<div class="upload-panel">', unsafe_allow_html=True)

    adm_title = st.text_input("Notice Title", placeholder="e.g. End Semester Exams Timetable")
    col_b, col_y, col_p = st.columns(3)
    with col_b:
        adm_branch = st.selectbox(
            "Target Branch",
            ["All", "Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil"],
        )
    with col_y:
        adm_year = st.selectbox("Target Year", ["All", "1st Year", "2nd Year", "3rd Year", "4th Year"])
    with col_p:
        adm_priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    input_mode = st.radio("Input Method", ["Manual Text Entry", "Upload Document / Scan"], horizontal=True)

    doc_text = ""
    if input_mode == "Manual Text Entry":
        doc_text = st.text_area("Notice content", height=200, placeholder="Type or paste notice text...")
    else:
        uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf"])
        if uploaded_file is not None:
            st.success(f"File ready: {uploaded_file.name}")
            if st.button("🔍 Run AI OCR Extraction", use_container_width=True):
                with st.spinner("Extracting text..."):
                    temp_path = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        uploaded_file.name,
                    )
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    extracted = perform_ocr_fn(temp_path) if fallback_available else "[OCR unavailable]"
                    st.session_state.ocr_cache = extracted
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass
        if st.session_state.ocr_cache:
            doc_text = st.text_area(
                "Review extracted text",
                value=st.session_state.ocr_cache,
                height=200,
            )

    if st.button("🧠 Preview AI Analysis", use_container_width=True):
        if not doc_text:
            st.warning("Please provide notice text first.")
        else:
            st.session_state.ai_preview = {
                "category": predict_category(doc_text),
                "summary": generate_summary(doc_text, max_sentences=2),
                "deadlines": detect_deadlines(doc_text),
            }

    final_category = "General"
    if st.session_state.ai_preview:
        ap = st.session_state.ai_preview
        st.success(f"Category: **{ap['category']}** · Summary ready · Deadlines: `{ap['deadlines'] or 'None'}`")
        cats = ["Exams", "Placements", "Events", "Assignments", "Workshops", "General"]
        idx = cats.index(ap["category"]) if ap["category"] in cats else 5
        final_category = st.selectbox("Category Override", cats, index=idx)

    if st.button("🚀 Publish Notice", type="primary", use_container_width=True):
        if not adm_title or not doc_text:
            st.error("Title and content are required.")
        else:
            final_cat = final_category if st.session_state.ai_preview else predict_category(doc_text)
            final_sum = (
                st.session_state.ai_preview["summary"]
                if st.session_state.ai_preview
                else generate_summary(doc_text, max_sentences=2)
            )
            final_dead = (
                st.session_state.ai_preview["deadlines"]
                if st.session_state.ai_preview
                else detect_deadlines(doc_text)
            )

            if api_online:
                try:
                    payload = {
                        "title": adm_title,
                        "branch": adm_branch,
                        "year": adm_year,
                        "priority": adm_priority,
                        "content": doc_text,
                        "category": final_cat,
                    }
                    res = requests.post(f"{BACKEND_URL}/api/notices", data=payload)
                    if res.json().get("success"):
                        st.success("Notice published successfully!")
                        st.session_state.ocr_cache = ""
                        st.session_state.ai_preview = None
                        st.rerun()
                    else:
                        st.error("Failed to publish notice.")
                except Exception as exc:
                    st.error(f"Error: {exc}")
            else:
                res = add_notice_fn(
                    title=adm_title,
                    content=doc_text,
                    summary=final_sum,
                    category=final_cat,
                    branch=adm_branch,
                    year=adm_year,
                    priority=adm_priority,
                    deadlines=final_dead,
                    file_path=None,
                )
                if res["success"]:
                    st.success("Notice published!")
                    st.session_state.ocr_cache = ""
                    st.session_state.ai_preview = None
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_settings_page(user, load_all_notices, pin_action, unpin_action, delete_action):
    """User settings and admin notice management."""
    render_page_header(
        "⚙ Settings",
        "Manage your profile and notice administration.",
    )

    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("#### Profile")
    st.markdown(f"""
    <div class="settings-row"><span class="settings-label">Username</span><span class="settings-value">{esc(user['username'])}</span></div>
    <div class="settings-row"><span class="settings-label">Role</span><span class="settings-value">{user['role'].title()}</span></div>
    """, unsafe_allow_html=True)
    if user.get("email"):
        st.markdown(
            f'<div class="settings-row"><span class="settings-label">Email</span>'
            f'<span class="settings-value">{esc(user["email"])}</span></div>',
            unsafe_allow_html=True,
        )
    if user["role"] == "student":
        st.markdown(f"""
        <div class="settings-row"><span class="settings-label">Branch</span><span class="settings-value">{esc(user.get('branch', 'N/A'))}</span></div>
        <div class="settings-row"><span class="settings-label">Year</span><span class="settings-value">{esc(user.get('year', 'N/A'))}</span></div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if user["role"] != "admin":
        return

    st.markdown("---")
    st.markdown("### Notice Management")
    st.caption("Pin, unpin, or delete notices from the platform.")

    adm_notices = load_all_notices(branch="All", year="All")
    manage_search, manage_category, manage_priority, manage_pin_filter = render_search_panel(
        key_prefix="admin_manage",
        show_pin_filter=True,
    )
    filtered = filter_admin_notices(
        adm_notices,
        search=manage_search,
        category=manage_category,
        priority=manage_priority,
        pin_filter=manage_pin_filter,
    )
    render_search_results_bar(
        len(filtered), len(adm_notices), manage_search,
        manage_category, manage_priority, pin_filter=manage_pin_filter,
    )

    if not adm_notices:
        st.info("No notices published yet.")
    elif not filtered:
        st.warning("No notices match your filters.")
    else:
        for notice in filtered:
            render_admin_manage_card(
                notice, manage_search, pin_action, unpin_action, delete_action,
            )
