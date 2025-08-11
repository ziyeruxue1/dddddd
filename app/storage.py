from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from typing import Iterator, List, Dict, Any, Tuple

DATA_DIR = "/workspace/data"
DB_PATH = "/workspace/data/app.db"

os.makedirs(DATA_DIR, exist_ok=True)


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS hs300_prices (
                date TEXT PRIMARY KEY,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                amount REAL
            )
            """
        )
        conn.commit()


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def fetch_all_prices(conn: sqlite3.Connection) -> List[Tuple]:
    cur = conn.execute(
        "SELECT date, open, high, low, close, volume, amount FROM hs300_prices ORDER BY date ASC"
    )
    return cur.fetchall()


def upsert_prices(conn: sqlite3.Connection, prices: List[Dict[str, Any]]) -> Tuple[int, int]:
    inserted = 0
    updated = 0
    for row in sorted(prices, key=lambda r: r["date"]):
        d = row["date"].isoformat() if hasattr(row["date"], "isoformat") else str(row["date"])  # ensure string
        cur = conn.execute("SELECT 1 FROM hs300_prices WHERE date = ?", (d,))
        exists = cur.fetchone() is not None
        if exists:
            conn.execute(
                """
                UPDATE hs300_prices
                SET open = ?, high = ?, low = ?, close = ?, volume = ?, amount = ?
                WHERE date = ?
                """,
                (
                    row.get("open"),
                    row.get("high"),
                    row.get("low"),
                    row.get("close"),
                    row.get("volume"),
                    row.get("amount"),
                    d,
                ),
            )
            updated += 1
        else:
            conn.execute(
                """
                INSERT INTO hs300_prices (date, open, high, low, close, volume, amount)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    d,
                    row.get("open"),
                    row.get("high"),
                    row.get("low"),
                    row.get("close"),
                    row.get("volume"),
                    row.get("amount"),
                ),
            )
            inserted += 1
    conn.commit()
    return inserted, updated