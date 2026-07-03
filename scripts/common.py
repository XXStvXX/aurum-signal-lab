from __future__ import annotations

import json
import math
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DATA = ROOT / "public" / "data"
EVENTS_FILE = ROOT / "data" / "events" / "gold_events_seed.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        if PUBLIC_DATA in path.parents:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        else:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def parse_day(value: str) -> date:
    return datetime.strptime(value[:10], "%Y-%m-%d").date()


def tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", text.lower())
    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "are",
        "was",
        "were",
        "has",
        "have",
        "gold",
        "xau",
        "usd",
    }
    return {token for token in tokens if token not in stopwords}


def classify_event(text: str) -> dict[str, Any]:
    lower = text.lower()
    patterns = [
        ("war", ["war", "missile", "attack", "invasion", "airstrike", "escalation", "conflict"]),
        ("fed_policy", ["federal reserve", "fed", "fomc", "powell", "rate cut", "rate hike", "interest rate"]),
        ("inflation", ["inflation", "cpi", "pce", "prices", "disinflation"]),
        ("banking_crisis", ["bank", "banking", "credit suisse", "liquidity", "deposit", "regional bank"]),
        ("sovereign_debt", ["debt ceiling", "downgrade", "treasury", "sovereign", "default"]),
        ("usd_rates", ["dollar", "dxy", "yield", "treasury yield", "real yield"]),
        ("central_bank_gold", ["central bank", "gold reserves", "pboc", "purchases", "reserve buying"]),
    ]
    scores: dict[str, int] = {}
    for category, terms in patterns:
        scores[category] = sum(1 for term in terms if term in lower)
    category = max(scores, key=scores.get)
    if scores[category] == 0:
        category = "market_news"

    bullish_categories = {"war", "banking_crisis", "sovereign_debt", "central_bank_gold"}
    bearish_categories = {"fed_policy", "usd_rates"}
    if category in bullish_categories:
        direction = "bullish_gold"
    elif category in bearish_categories:
        direction = "context_dependent"
    else:
        direction = "neutral_watch"

    intensity = min(100, 35 + scores.get(category, 0) * 18 + sum(scores.values()) * 4)
    return {
        "category": category,
        "direction": direction,
        "intensity": intensity,
        "matched_terms": {key: value for key, value in scores.items() if value},
    }


def synthetic_gold_price(day: date) -> float:
    """Deterministic fallback series for demos and offline tests."""
    base = 900 + (day.year - 2000) * 72
    seasonal = math.sin(day.toordinal() / 37.0) * 55
    trend = (day.toordinal() % 730) * 0.05
    return round(base + seasonal + trend, 2)


def nearest_trading_day(prices: dict[date, float], target: date) -> date | None:
    for distance in range(0, 8):
        for candidate in (target - timedelta(days=distance), target + timedelta(days=distance)):
            if candidate in prices:
                return candidate
    return None
