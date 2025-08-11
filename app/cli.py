from __future__ import annotations

from .storage import init_db, get_conn, upsert_prices
from .fetcher import fetch_hs300_history


def update_all() -> None:
    init_db()
    with get_conn() as conn:
        prices = fetch_hs300_history()
        inserted, updated = upsert_prices(conn, prices)
        print(f"Inserted: {inserted}, Updated: {updated}")


if __name__ == "__main__":
    update_all()