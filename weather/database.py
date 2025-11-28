# weather/database.py
import sqlite3
from weather.api import get_weather_description  # ← ВОТ СЮДА!
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "weather_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            city TEXT NOT NULL,
            temperature REAL NOT NULL,
            windspeed REAL,
            winddirection INTEGER,
            weathercode INTEGER,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_request(city: str, data: dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    desc = data.get('description', get_weather_description(data['weathercode']))
    cursor.execute("""
        INSERT INTO history 
        (timestamp, city, temperature, windspeed, winddirection, weathercode, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        city,
        data['temperature'],
        data.get('windspeed'),
        data.get('winddirection'),
        data['weathercode'],
        desc
    ))
    conn.commit()
    conn.close()

def get_history(limit: int = 10):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, city, temperature, description 
        FROM history 
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows