"""Shared business logic used by the Flask API and dashboard fallback mode."""


def registration_http_status(result):
    """Maps a registration result dict to an HTTP status code."""
    if result.get("success"):
        return 200
    message = result.get("message", "").lower()
    if "restricted" in message or "email" in message and "required" in message:
        return 403
    return 400


def process_notice_ai_pipeline(content, manual_category="", predict_category_fn=None,
                               generate_summary_fn=None, detect_deadlines_fn=None):
    """
    Runs classification, summarization, and deadline detection on notice content.
    Dependency functions are injected so this module stays free of heavy imports.
    """
    if not predict_category_fn or not generate_summary_fn or not detect_deadlines_fn:
        raise ValueError("AI pipeline functions must be provided.")

    category = manual_category if manual_category else predict_category_fn(content)
    summary = generate_summary_fn(content, max_sentences=3)
    deadlines = detect_deadlines_fn(content)
    return category, summary, deadlines


def build_recommendations(notices, branch="All", year="All"):
    """Scores and sorts notices for the smart recommendations endpoint."""
    recommendations = []
    for notice in notices:
        score = 0
        priority = notice.get("priority")
        if priority == "High":
            score += 10
        elif priority == "Medium":
            score += 5

        if notice.get("branch") == branch and branch != "All":
            score += 8
        if notice.get("year") == year and year != "All":
            score += 5

        notice_copy = dict(notice)
        notice_copy["recommendation_score"] = score
        recommendations.append(notice_copy)

    recommendations.sort(key=lambda item: item["recommendation_score"], reverse=True)
    return recommendations
