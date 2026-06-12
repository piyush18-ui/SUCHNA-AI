"""
SQLite persistence layer for the AI NoticeBoard.

Schema upgrades are applied automatically via init_db() -> _migrate_schema()
so existing noticeboard.db files remain compatible across versions.
"""

import os
import re
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

from config import ALLOWED_ADMIN_DOMAINS, ALLOWED_ADMIN_EMAILS

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'noticeboard.db')

def get_db_connection():
    """Establishes a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _migrate_schema(cursor):
    """Applies backward-compatible schema upgrades for existing databases."""
    cursor.execute("PRAGMA table_info(notices)")
    notice_columns = {row[1] for row in cursor.fetchall()}

    if 'is_pinned' not in notice_columns:
        cursor.execute('ALTER TABLE notices ADD COLUMN is_pinned INTEGER DEFAULT 0')
        print("Migration: added notices.is_pinned column.")

    cursor.execute("PRAGMA table_info(users)")
    user_columns = {row[1] for row in cursor.fetchall()}

    if 'email' not in user_columns:
        cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')
        cursor.execute(
            'CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email '
            'ON users(email) WHERE email IS NOT NULL'
        )
        print("Migration: added users.email column.")


def init_db():
    """Initializes the database tables if they do not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            role TEXT NOT NULL CHECK(role IN ('admin', 'student')),
            branch TEXT DEFAULT 'All',
            year TEXT DEFAULT 'All',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Notices Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            summary TEXT,
            category TEXT NOT NULL CHECK(category IN ('Exams', 'Placements', 'Events', 'Assignments', 'Workshops', 'General')),
            branch TEXT NOT NULL DEFAULT 'All',
            year TEXT NOT NULL DEFAULT 'All',
            priority TEXT NOT NULL CHECK(priority IN ('High', 'Medium', 'Low')) DEFAULT 'Medium',
            deadlines TEXT,  -- comma-separated strings of detected dates
            file_path TEXT,  -- path to uploaded document/image
            is_pinned INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''');
    
    _migrate_schema(cursor)
    conn.commit()
    conn.close()
    print("Database tables initialized successfully.")

# --- User Management Functions ---

def validate_email_format(email):
    """Returns (is_valid, error_message) for a basic email format check."""
    if not email or not EMAIL_PATTERN.match(email.strip()):
        return False, "Please enter a valid email address."
    return True, None


def validate_admin_email(email):
    """
    Allow any institutional email ending with .edu, .edu.in or .ac.in
    """
    is_valid, error_message = validate_email_format(email)
    if not is_valid:
        return False, error_message

    normalized_email = email.strip().lower()
    domain = normalized_email.split("@")[-1]

    if (
        domain.endswith("edu")
        or domain.endswith("edu.in")
        or domain.endswith("ac.in")
    ):
        return True, None

    return False, (
        "Please use a valid institutional email ending with .edu, .edu.in or .ac.in"
    )

def register_user(username, password, role, branch='All', year='All', email=None):
    """Registers a new user in the system with a hashed password."""
    if role == 'admin':
        if not email:
            return {
                "success": False,
                "message": "Admin accounts require a valid institutional email address.",
            }
        is_allowed, error_message = validate_admin_email(email)
        if not is_allowed:
            return {"success": False, "message": error_message}
        email = email.strip().lower()
    elif email:
        is_valid, error_message = validate_email_format(email)
        if not is_valid:
            return {"success": False, "message": error_message}
        email = email.strip().lower()

    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pwd = generate_password_hash(password)

    try:
        cursor.execute('''
            INSERT INTO users (username, password, email, role, branch, year)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, hashed_pwd, email, role, branch, year))
        conn.commit()
        user_id = cursor.lastrowid
        return {"success": True, "user_id": user_id, "message": "Registration successful."}
    except sqlite3.IntegrityError as exc:
        error_text = str(exc).lower()
        if "email" in error_text:
            return {"success": False, "message": "This email is already registered."}
        return {"success": False, "message": "Username already exists."}
    finally:
        conn.close()


def authenticate_user(username, password):
    """Authenticates a user against stored hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        user_data = dict(user)
        return {
            "success": True,
            "user": {
                "id": user_data["id"],
                "username": user_data["username"],
                "role": user_data["role"],
                "branch": user_data["branch"],
                "year": user_data["year"],
                "email": user_data.get("email"),
            }
        }
    return {"success": False, "message": "Invalid username or password."}

# --- Notice Management Functions ---

def add_notice(title, content, summary, category, branch='All', year='All', priority='Medium', deadlines=None, file_path=None):
    """Inserts a new notice into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO notices (title, content, summary, category, branch, year, priority, deadlines, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, summary, category, branch, year, priority, deadlines, file_path))
        conn.commit()
        notice_id = cursor.lastrowid
        return {"success": True, "notice_id": notice_id, "message": "Notice added successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error adding notice: {str(e)}"}
    finally:
        conn.close()

def delete_notice(notice_id):
    """Deletes a notice by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First retrieve file_path to delete the actual file if present
        cursor.execute('SELECT file_path FROM notices WHERE id = ?', (notice_id,))
        row = cursor.fetchone()
        if row and row['file_path']:
            # Safe delete of the file on disk
            try:
                if os.path.exists(row['file_path']):
                    os.remove(row['file_path'])
            except Exception as fe:
                print(f"Error removing file {row['file_path']}: {fe}")
                
        cursor.execute('DELETE FROM notices WHERE id = ?', (notice_id,))
        conn.commit()
        return {"success": True, "message": "Notice deleted successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error deleting notice: {str(e)}"}
    finally:
        conn.close()

def normalize_search_query(search_query):
    """Strips and validates a search string; returns None when empty."""
    if not search_query or not isinstance(search_query, str):
        return None
    cleaned = search_query.strip()
    return cleaned if cleaned else None


def get_notices(branch=None, year=None, category=None, priority=None, search_query=None):
    """Fetches notices based on filtering criteria."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM notices WHERE 1=1"
    params = []

    # Standard filtering logic
    if branch and branch != 'All':
        query += " AND (branch = ? OR branch = 'All')"
        params.append(branch)
    if year and year != 'All':
        query += " AND (year = ? OR year = 'All')"
        params.append(year)
    if category and category != 'All':
        query += " AND category = ?"
        params.append(category)
    if priority and priority != 'All':
        query += " AND priority = ?"
        params.append(priority)

    search_query = normalize_search_query(search_query)
    if search_query:
        query += (
            " AND (LOWER(title) LIKE ? OR LOWER(content) LIKE ? "
            "OR LOWER(category) LIKE ? OR LOWER(COALESCE(summary, '')) LIKE ?)"
        )
        search_wildcard = f"%{search_query.lower()}%"
        params.extend([search_wildcard, search_wildcard, search_wildcard, search_wildcard])
        
    query += " ORDER BY is_pinned DESC, created_at DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Convert list of Rows into dicts
    notices = []
    for r in rows:
        notices.append(dict(r))
        
    conn.close()
    return notices

def get_notice_by_id(notice_id):
    """Fetches a single notice by its database ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM notices WHERE id = ?', (notice_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def pin_notice(notice_id):
    """Pins a notice so it appears at the top of the dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id FROM notices WHERE id = ?', (notice_id,))
        if not cursor.fetchone():
            return {"success": False, "message": "Notice not found."}

        cursor.execute('UPDATE notices SET is_pinned = 1 WHERE id = ?', (notice_id,))
        conn.commit()
        return {"success": True, "message": "Notice pinned successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error pinning notice: {str(e)}"}
    finally:
        conn.close()


def unpin_notice(notice_id):
    """Removes pin status from a notice."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id FROM notices WHERE id = ?', (notice_id,))
        if not cursor.fetchone():
            return {"success": False, "message": "Notice not found."}

        cursor.execute('UPDATE notices SET is_pinned = 0 WHERE id = ?', (notice_id,))
        conn.commit()
        return {"success": True, "message": "Notice unpinned successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error unpinning notice: {str(e)}"}
    finally:
        conn.close()
