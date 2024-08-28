""" 
chats_db.py
This module provides functions for creating a SQLite database, saving chat sessions, loading saved chats, loading chat messages, deleting chats, and managing the selected AI model.
"""
import sqlite3
import json
import logging

# Database name
DATABASE_NAME = 'chats.db'

# Default model to use if none is set
DEFAULT_MODEL = 'llama3.1'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chats_db")

def create_database():
    """Create the database, chats table, and settings table if they do not exist."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Create chats table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_name TEXT,
                    messages TEXT,
                    model TEXT
                )
            ''')
            
            # Create settings table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            # Insert default model if it doesn't exist
            cursor.execute('''
                INSERT OR IGNORE INTO settings (key, value)
                VALUES ('default_model', 'llama3.1')
            ''')
            
            conn.commit()
            logger.info("Database, tables, and default settings created successfully")
    except sqlite3.Error as e:
        logger.error(f"Error accessing database: {e}")
        raise

def save_chat(chat_name, messages, model):
    """Save a chat with the given name, messages, and model."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO chats (chat_name, messages, model) VALUES (?, ?, ?)', 
                           (chat_name, json.dumps(messages), model))
            conn.commit()
            logger.info(f"Chat '{chat_name}' saved successfully with model {model}")
    except sqlite3.Error as e:
        logger.error(f"Error saving chat: {e}")
        raise

def load_chats():
    """Load all chats from the database."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, chat_name, model FROM chats')
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
            cursor.execute('SELECT messages, model FROM chats WHERE id = ?', (chat_id,))
            result = cursor.fetchone()
            if result:
                messages = json.loads(result[0])
                model = result[1]
                logger.info(f"Successfully loaded messages for chat ID {chat_id} with model {model}")
                return True, messages, model
            else:
                logger.warning(f"No chat found with id: {chat_id}")
                return False, None, None
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

def get_default_model():
    """Get the default model from the settings table."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM settings WHERE key = "default_model"')
            result = cursor.fetchone()
            return result[0] if result else DEFAULT_MODEL # Fallback to default model if no default is set
    except sqlite3.Error as e:
        logger.error(f"Error getting default model: {e}")
        return DEFAULT_MODEL # Fallback to default model in case of error

def set_default_model(model):
    """Set the default model in the settings table."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE settings SET value = ? WHERE key = "default_model"', (model,))
            conn.commit()
            logger.info(f"Default model updated to {model}")
    except sqlite3.Error as e:
        logger.error(f"Error setting default model: {e}")
        raise
