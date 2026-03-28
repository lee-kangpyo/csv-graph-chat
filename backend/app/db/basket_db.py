import sqlite3
import json
import os
from datetime import datetime
from typing import Optional

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "basket.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS baskets (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            graph_config TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_basket(basket_id: str, name: str, graph_config: dict) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO baskets (id, name, graph_config, created_at) VALUES (?, ?, ?, ?)",
        (basket_id, name, json.dumps(graph_config), created_at),
    )
    conn.commit()
    conn.close()
    return {
        "id": basket_id,
        "name": name,
        "graph_config": graph_config,
        "created_at": created_at,
    }


def get_basket(basket_id: str) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM baskets WHERE id = ?", (basket_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row["id"],
            "name": row["name"],
            "graph_config": json.loads(row["graph_config"]),
            "created_at": row["created_at"],
        }
    return None


def get_all_baskets() -> list[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM baskets ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "graph_config": json.loads(row["graph_config"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def delete_basket(basket_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM baskets WHERE id = ?", (basket_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


init_db()
