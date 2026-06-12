import os

# Flask REST API base URL used by the Streamlit dashboard.
BACKEND_URL = os.environ.get(
    "BACKEND_URL",
    "https://ai-noticeboard-pn3r.onrender.com",
).rstrip("/")

# Authorized admin email addresses (exact match, case-insensitive).
# Override via ALLOWED_ADMIN_EMAILS env var (comma-separated).
ALLOWED_ADMIN_EMAILS = [
    email.strip().lower()
    for email in os.environ.get(
        "ALLOWED_ADMIN_EMAILS",
        "admin@college.edu,admin@university.ac.in",
    ).split(",")
    if email.strip()
]

# Authorized email domains for admin registration.
# Override via ALLOWED_ADMIN_DOMAINS env var (comma-separated).
ALLOWED_ADMIN_DOMAINS = [
    domain.strip().lower()
    for domain in os.environ.get(
        "ALLOWED_ADMIN_DOMAINS",
        "college.edu,university.ac.in",
    ).split(",")
    if domain.strip()
]
