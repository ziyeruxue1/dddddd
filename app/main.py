from __future__ import annotations

from typing import List
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route
from starlette.templating import Jinja2Templates

from .storage import init_db, get_conn, fetch_all_prices, upsert_prices
from .fetcher import fetch_hs300_history


templates = Jinja2Templates(directory="/workspace/templates")


async def homepage(request: Request) -> HTMLResponse:
    with get_conn() as conn:
        rows = fetch_all_prices(conn)
        labels: List[str] = [r[0] for r in rows]
        open_values = [r[1] for r in rows]
        high_values = [r[2] for r in rows]
        low_values = [r[3] for r in rows]
        close_values = [r[4] for r in rows]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "labels": labels,
            "close_values": close_values,
            "open_values": open_values,
            "high_values": high_values,
            "low_values": low_values,
            "count": len(labels),
        },
    )


async def update(request: Request) -> JSONResponse:
    with get_conn() as conn:
        prices = fetch_hs300_history()
        inserted, updated = upsert_prices(conn, prices)
        total = conn.execute("SELECT COUNT(1) FROM hs300_prices").fetchone()[0]
    return JSONResponse({"inserted": inserted, "updated": updated, "total": total})


routes = [
    Route("/", endpoint=homepage, methods=["GET"]),
    Route("/update", endpoint=update, methods=["GET", "POST"]),
]


@asynccontextmanager
async def lifespan(app: Starlette):
    init_db()
    yield


app = Starlette(routes=routes, lifespan=lifespan)