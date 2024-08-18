""" 
chats_db.py
This module provides functions for creating a SQLite database, saving chat sessions, loading saved chats, loading chat messages, and deleting chats.
"""
import sqlite3
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chats_db")

DATABASE_NAME = 'chats.db'

def create_database():
    """Create the database and chats table if they do not exist."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Check if the table already exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chats'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                cursor.execute('''
                    CREATE TABLE chats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_name TEXT,
                        messages TEXT
                    )
                ''')
                conn.commit()
                logger.info("Database and chats table created successfully")
            else:
                logger.debug("Chats table already exists")
    except sqlite3.Error as e:
        logger.error(f"Error accessing database: {e}")
        raise

def save_chat(chat_name, messages):
    """Save a chat with the given name and messages."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO chats (chat_name, messages) VALUES (?, ?)', (chat_name, json.dumps(messages)))
            conn.commit()
            logger.info(f"Chat '{chat_name}' saved successfully")
    except sqlite3.Error as e:
        logger.error(f"Error saving chat: {e}")
        raise

def load_chats():
    """Load all chats from the database."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, chat_name FROM chats')
            chats = cursor.fetchall()
        logger.info(f"Successfully loaded {len(chats)} chats")
        return chats
    except sqlite3.Error as e:
        logger.error(f"Error loading chats: {e}")
        raise

def load_chat_messages(chat_id):
    """Load messages for a specific chat by ID."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT messages FROM chats WHERE id = ?', (chat_id,))
            result = cursor.fetchone()
            if result:
                messages = json.loads(result[0])
                logger.info(f"Successfully loaded messages for chat ID {chat_id}")
                return True, messages
            else:
                logger.warning(f"No chat found with id: {chat_id}")
                return False, None
    except sqlite3.Error as e:
        logger.error(f"Error loading chat messages: {e}")
        raise

def delete_chat(chat_id):
    """Delete a chat by ID."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM chats WHERE id = ?', (chat_id,))
            conn.commit()
            logger.info(f"Chat with ID {chat_id} deleted successfully")
    except sqlite3.Error as e:
        logger.error(f"Error deleting chat: {e}")
        raise
