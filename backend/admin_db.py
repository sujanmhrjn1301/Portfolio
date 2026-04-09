"""
Admin Credentials Database

Manages admin authentication separately from main database.
Stores hashed passwords for security.
"""

import sqlite3
import os
from hashlib import sha256
import logging

logger = logging.getLogger(__name__)

ADMIN_DB_PATH = "./admin_credentials.db"

def hash_password(password: str) -> str:
    """Hash password for secure storage"""
    return sha256(password.encode()).hexdigest()

def init_admin_db():
    """Initialize admin credentials database with default admin"""
    try:
        conn = sqlite3.connect(ADMIN_DB_PATH)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add default admin if it doesn't exist
        try:
            default_username = "eiji"
            default_password = "iamsujanmaharjan"
            password_hash = hash_password(default_password)
            
            cursor.execute(
                'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                (default_username, password_hash)
            )
            conn.commit()
            logger.info("✅ Admin database initialized with default admin")
        except sqlite3.IntegrityError:
            # Admin already exists
            pass
        
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Error initializing admin database: {str(e)}")

def verify_admin_credentials(username: str, password: str) -> bool:
    """
    Verify admin credentials against database
    
    Returns True if credentials are valid, False otherwise
    """
    try:
        if not os.path.exists(ADMIN_DB_PATH):
            init_admin_db()
        
        conn = sqlite3.connect(ADMIN_DB_PATH)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            'SELECT id FROM admins WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    except Exception as e:
        logger.error(f"❌ Error verifying admin credentials: {str(e)}")
        return False

def add_admin(username: str, password: str) -> bool:
    """Add a new admin user"""
    try:
        if not os.path.exists(ADMIN_DB_PATH):
            init_admin_db()
        
        conn = sqlite3.connect(ADMIN_DB_PATH)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        conn.close()
        
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
        
        conn = sqlite3.connect(ADMIN_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, created_at FROM admins')
        admins = cursor.fetchall()
        conn.close()
        
        return admins
    
    except Exception as e:
        logger.error(f"❌ Error fetching admins: {str(e)}")
        return []
