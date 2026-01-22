import sqlite3
import datetime
import os

# Define the DB path relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'procrastination.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            time_of_day TEXT,
            task_type TEXT,
            subtask_size TEXT,
            outcome TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def log_interaction(task_type, subtask_size, outcome="suggested"):
    try:
        conn = get_connection()
        c = conn.cursor()
        now = datetime.datetime.now()
        timestamp = now.isoformat()
        
        # Determine time of day roughly
        hour = now.hour
        if 5 <= hour < 12:
            time_of_day = "Morning"
        elif 12 <= hour < 17:
            time_of_day = "Afternoon"
        elif 17 <= hour < 21:
            time_of_day = "Evening"
        else:
            time_of_day = "Night"

        c.execute('''
            INSERT INTO interactions (timestamp, time_of_day, task_type, subtask_size, outcome)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, time_of_day, task_type, subtask_size, outcome))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging interaction: {e}")

def fetch_history(limit=10):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM interactions ORDER BY id DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

if __name__ == "__main__":
    init_db()
