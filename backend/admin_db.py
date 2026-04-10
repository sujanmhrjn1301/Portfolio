"""
Admin Credentials Database

Manages admin authentication separately from main database.
Stores hashed passwords for security using bcrypt.
"""

import sqlite3
import os
import bcrypt
import logging

logger = logging.getLogger(__name__)

ADMIN_DB_PATH = "./admin_credentials.db"

def hash_password(password: str) -> str:
    """Hash password using bcrypt for secure storage"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def init_admin_db():
    """Initialize admin credentials database (no default admin)"""
    try:
        with sqlite3.connect(ADMIN_DB_PATH) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    except Exception as e:
        logger.error(f"❌ Error initializing admin database: {str(e)}")

def verify_admin_credentials(username: str, password: str) -> bool:
    """Verify admin credentials against database"""
    try:
        if not os.path.exists(ADMIN_DB_PATH):
            init_admin_db()
        with sqlite3.connect(ADMIN_DB_PATH) as conn:
            cursor = conn.execute(
                'SELECT password_hash FROM admins WHERE username = ?',
                (username,)
            )
            row = cursor.fetchone()
        if row:
            stored_hash = row[0].encode()
            return bcrypt.checkpw(password.encode(), stored_hash)
        return False
    except Exception as e:
        logger.error(f"❌ Error verifying admin credentials: {str(e)}")
        return False

def add_admin(username: str, password: str) -> bool:
    """Add a new admin user"""
    try:
        if not os.path.exists(ADMIN_DB_PATH):
            init_admin_db()
        password_hash = hash_password(password)
        with sqlite3.connect(ADMIN_DB_PATH) as conn:
            conn.execute(
                'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
        logger.info(f"✅ Admin user '{username}' added successfully")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"❌ Admin user '{username}' already exists")
        return False
    except Exception as e:
        logger.error(f"❌ Error adding admin user: {str(e)}")
        return False

def get_all_admins() -> list:
    """Get all admin usernames (for debugging)"""
    try:
        if not os.path.exists(ADMIN_DB_PATH):
            init_admin_db()
        with sqlite3.connect(ADMIN_DB_PATH) as conn:
            cursor = conn.execute('SELECT username, created_at FROM admins')
            admins = cursor.fetchall()
        return admins
    except Exception as e:
        logger.error(f"❌ Error fetching admins: {str(e)}")
        return []
