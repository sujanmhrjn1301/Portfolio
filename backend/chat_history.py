import sqlite3
import json
from datetime import datetime
from typing import List, Dict
import uuid

class ChatHistory:
    def __init__(self, db_path: str = "./chat_history.db"):
        """Initialize chat history database"""
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Create database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create conversations table
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                     (id TEXT PRIMARY KEY,
                      title TEXT,
                      created_at TEXT,
                      updated_at TEXT,
                      is_shared INTEGER DEFAULT 0,
                      share_id TEXT UNIQUE)''')
        
        # Create messages table
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id TEXT PRIMARY KEY,
                      conversation_id TEXT,
                      role TEXT,
                      content TEXT,
                      created_at TEXT,
                      FOREIGN KEY(conversation_id) REFERENCES conversations(id))''')
        
        conn.commit()
        conn.close()
    
    def create_conversation(self, title: str = "New Chat") -> str:
        """Create a new conversation"""
        conv_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''INSERT INTO conversations (id, title, created_at, updated_at)
                     VALUES (?, ?, ?, ?)''',
                  (conv_id, title, now, now))
        
        conn.commit()
        conn.close()
        
        return conv_id
    
    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to a conversation"""
        msg_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''INSERT INTO messages (id, conversation_id, role, content, created_at)
                     VALUES (?, ?, ?, ?, ?)''',
                  (msg_id, conversation_id, role, content, now))
        
        # Update conversation's updated_at
        c.execute('''UPDATE conversations SET updated_at = ? WHERE id = ?''',
                  (now, conversation_id))
        
        conn.commit()
        conn.close()
        
        return msg_id
    
    def get_conversation_messages(self, conversation_id: str) -> List[Dict]:
        """Get all messages from a conversation"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''SELECT id, role, content, created_at FROM messages
                     WHERE conversation_id = ?
                     ORDER BY created_at ASC''', (conversation_id,))
        
        messages = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return messages
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations for the user (not shared ones)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''SELECT id, title, created_at, updated_at, is_shared
                     FROM conversations
                     ORDER BY updated_at DESC''')
        
        conversations = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return conversations
    
    def share_conversation(self, conversation_id: str) -> str:
        """Generate a share link for a conversation"""
        share_id = str(uuid.uuid4())[:8]  # Short share ID
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''UPDATE conversations SET is_shared = 1, share_id = ?
                     WHERE id = ?''', (share_id, conversation_id))
        
        conn.commit()
        conn.close()
        
        return share_id
    
    def get_shared_conversation(self, share_id: str) -> Dict:
        """Get a shared conversation by share ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''SELECT id, title, created_at FROM conversations
                     WHERE share_id = ? AND is_shared = 1''', (share_id,))
        
        conversation = dict(c.fetchone() or {})
        
        if conversation:
            conv_id = conversation['id']
            c.execute('''SELECT role, content, created_at FROM messages
                         WHERE conversation_id = ?
                         ORDER BY created_at ASC''', (conv_id,))
            
            messages = [dict(row) for row in c.fetchall()]
            conversation['messages'] = messages
        
        conn.close()
        
        return conversation
    
    def delete_conversation(self, conversation_id: str):
        """Delete a conversation and its messages"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Delete messages first
        c.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
        # Delete conversation
        c.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
        
        conn.commit()
        conn.close()
    
    def update_conversation(self, conversation_id: str, title: str):
        """Update conversation title"""
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''UPDATE conversations SET title = ?, updated_at = ?
                     WHERE id = ?''',
                  (title, now, conversation_id))
        
        conn.commit()
        conn.close()
