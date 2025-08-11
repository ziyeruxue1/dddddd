from __future__ import annotations

from datetime import datetime, date
from typing import List, Dict, Any

import requests

EASTMONEY_KLINE_URL = "https://push2his.eastmoney.com/api/qt/stock/kline/get"


def fetch_hs300_history() -> List[Dict[str, Any]]:
    """Fetch historical daily data for CSI 300 (沪深300) via Eastmoney API.

    Returns a list of dicts with keys: date, open, high, low, close, volume, amount.
    """
    params = {
        "secid": "1.000300",  # 1 = SH, 000300 = 沪深300指数
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "klt": "101",  # 101 = 日K
        "fqt": "1",  # 前复权
        "beg": "19900101",
        "end": "20500101",
    }
    headers = {
        "Referer": "https://quote.eastmoney.com/",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        ),
    }

    resp = requests.get(EASTMONEY_KLINE_URL, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    j = resp.json()
    data = j.get("data") or {}
    klines = data.get("klines") or []

    prices: List[Dict[str, Any]] = []
    for line in klines:
        parts = str(line).split(",")
        if len(parts) < 7:
            continue
        try:
            d: date = datetime.strptime(parts[0], "%Y-%m-%d").date()
            open_v = float(parts[1]) if parts[1] != "" else None
            close_v = float(parts[2]) if parts[2] != "" else None
            high_v = float(parts[3]) if parts[3] != "" else None
            low_v = float(parts[4]) if parts[4] != "" else None
            volume_v = float(parts[5]) if parts[5] != "" else None
            amount_v = float(parts[6]) if parts[6] != "" else None
        except Exception:
            continue
        prices.append(
            {
                "date": d,
                "open": open_v,
                "high": high_v,
                "low": low_v,
                "close": close_v,
                "volume": volume_v,
                "amount": amount_v,
            }
        )

    return prices