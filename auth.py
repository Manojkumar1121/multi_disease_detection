"""
Authentication and SQLite database persistence module.
Enforces bcrypt hashing, normalized usernames, minimum password lengths,
and parameterized SQL queries.
"""

import os
import sqlite3
import json
from typing import Optional, Dict, Any, List, Tuple
import bcrypt

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "app.db")
MIN_PASSWORD_LENGTH = 8


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Create a database connection and ensure directory exists."""
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Initialize database tables with parameterized DDL."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                patient_name TEXT,
                age INTEGER,
                symptoms TEXT,
                top_prediction TEXT,
                confidence REAL,
                top3_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()


def normalize_username(username: str) -> str:
    """Normalize username by trimming whitespace and converting to lowercase."""
    return username.strip().lower() if username else ""


def hash_password(password: str) -> str:
    """Hash password using bcrypt with salt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def check_password(password: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def register_user(
    username: str, password: str, db_path: str = DB_PATH
) -> Tuple[bool, str]:
    """
    Register a new user:
    - Normalizes username (strip, lowercase).
    - Enforces password length >= 8.
    - Hashes password with bcrypt.
    - Stores using parameterized SQL.

    Returns:
        (success, message)
    """
    clean_user = normalize_username(username)
    if not clean_user:
        return False, "Username cannot be empty."

    if len(clean_user) < 3:
        return False, "Username must be at least 3 characters long."

    if not password or len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."

    init_db(db_path)
    pwd_hash = hash_password(password)

    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (clean_user, pwd_hash),
            )
            conn.commit()
            return True, "Account created successfully! You can now log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose a different username."
    except Exception as e:
        return False, f"Registration error: {e}"


def authenticate_user(
    username: str, password: str, db_path: str = DB_PATH
) -> Optional[Dict[str, Any]]:
    """
    Authenticate user by normalized username and bcrypt password check.

    Returns:
        User dict {"id": int, "username": str} or None.
    """
    clean_user = normalize_username(username)
    if not clean_user or not password:
        return None

    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (clean_user,),
        )
        row = cursor.fetchone()
        if row and check_password(password, row["password_hash"]):
            return {"id": row["id"], "username": row["username"]}

    return None


def save_assessment(
    user_id: int,
    patient_name: str,
    age: int,
    symptoms: str,
    top_prediction: str,
    confidence: float,
    top3_json: str,
    db_path: str = DB_PATH,
) -> int:
    """Save an assessment record for the authenticated user."""
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO assessments (
                user_id, patient_name, age, symptoms, top_prediction, confidence, top3_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                patient_name.strip() if patient_name else "Anonymous",
                int(age) if age is not None else 0,
                symptoms,
                top_prediction,
                float(confidence),
                top3_json,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_user_assessments(
    user_id: int, db_path: str = DB_PATH
) -> List[Dict[str, Any]]:
    """Retrieve all assessment records belonging strictly to user_id."""
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, patient_name, age, symptoms, top_prediction, confidence, top3_json, created_at
            FROM assessments
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
