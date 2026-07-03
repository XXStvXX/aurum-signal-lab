from __future__ import annotations

import csv
import io
import urllib.error
import urllib.request
from datetime import date, timedelta

from common import EVENTS_FILE, PUBLIC_DATA, nearest_trading_day, parse_day, read_json, synthetic_gold_price, utc_now_iso, write_json


WINDOWS = [-30, -7, 0, 1, 3, 7, 30, 90, 180]


def fetch_stooq_gold(start: date, end: date) -> dict[date, float]:
    """Best-effort daily XAU/USD fetch from Stooq. Falls back upstream if unavailable."""
    d1 = start.strftime("%Y%m%d")
    d2 = end.strftime("%Y%m%d")
    url = f"https://stooq.com/q/d/l/?s=xauusd&i=d&d1={d1}&d2={d2}"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            text = response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError):
        return {}

    prices: dict[date, float] = {}
    for row in csv.DictReader(io.StringIO(text)):
        day_text = row.get("Date")
        close_text = row.get("Close")
        if not day_text or not close_text or close_text == "No data":
            continue
        try:
            prices[parse_day(day_text)] = float(close_text)
        except ValueError:
            continue
    return prices


def build_synthetic_prices(start: date, end: date) -> dict[date, float]:
    prices: dict[date, float] = {}
    current = start
    while current <= end:
        if current.weekday() < 5:
            prices[current] = synthetic_gold_price(current)
        current += timedelta(days=1)
    return prices


def price_at(prices: dict[date, float], event_day: date, offset: int) -> dict[str, object] | None:
    target = event_day + timedelta(days=offset)
    actual = nearest_trading_day(prices, target)
    if actual is None:
        return None
    return {"target_date": target.isoformat(), "actual_date": actual.isoformat(), "price": prices[actual]}


def enrich_event(event: dict[str, object], prices: dict[date, float]) -> dict[str, object]:
    event_day = parse_day(str(event["date"]))
    observations = {str(offset): price_at(prices, event_day, offset) for offset in WINDOWS}
    base = observations.get("0")
    returns: dict[str, float | None] = {}
    for offset in WINDOWS:
        point = observations.get(str(offset))
        if not point or not base:
            returns[str(offset)] = None
            continue
        returns[str(offset)] = round((float(point["price"]) / float(base["price"]) - 1) * 100, 3)

    enriched = dict(event)
    enriched["price_observations"] = observations
    enriched["gold_returns_pct_vs_event_day"] = returns
    enriched["short_term_bias"] = infer_bias(returns.get("7"))
    enriched["medium_term_bias"] = infer_bias(returns.get("30"))
    enriched["long_term_bias"] = infer_bias(returns.get("180"))
    return enriched


def infer_bias(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value > 1.0:
        return "bullish_realized"
    if value < -1.0:
        return "bearish_realized"
    return "flat_or_mixed"


def main() -> None:
    events = read_json(EVENTS_FILE)
    dates = [parse_day(event["date"]) for event in events]
    start = min(dates) - timedelta(days=45)
    end = max(dates) + timedelta(days=210)

    prices = fetch_stooq_gold(start, end)
    data_quality = "stooq_xauusd_daily" if prices else "synthetic_offline_fallback"
    if not prices:
        prices = build_synthetic_prices(start, end)

    payload = {
        "generated_at": utc_now_iso(),
        "data_quality": data_quality,
        "windows": WINDOWS,
        "events": [enrich_event(event, prices) for event in events],
    }
    write_json(PUBLIC_DATA / "event_studies.json", payload)


if __name__ == "__main__":
    main()
