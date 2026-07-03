from __future__ import annotations

from common import PUBLIC_DATA, tokenize, utc_now_iso, write_json, read_json


def event_text(event: dict[str, object]) -> str:
    channels = " ".join(event.get("expected_gold_channel", []) or [])
    return f"{event.get('title', '')} {event.get('category', '')} {event.get('region', '')} {event.get('summary', '')} {channels}"


def score(query_tokens: set[str], event_tokens: set[str]) -> float:
    if not query_tokens or not event_tokens:
        return 0.0
    overlap = len(query_tokens & event_tokens)
    union = len(query_tokens | event_tokens)
    return round(overlap / union, 4)


def main() -> None:
    studies = read_json(PUBLIC_DATA / "event_studies.json")
    live = read_json(PUBLIC_DATA / "live_signals.json")
    events = studies.get("events", [])

    indexed = [(event, tokenize(event_text(event))) for event in events]
    matches = []
    for signal in live.get("signals", []):
        query = tokenize(f"{signal.get('title', '')} {signal.get('category', '')} {signal.get('direction', '')}")
        ranked = []
        for event, tokens in indexed:
            similarity = score(query, tokens)
            if similarity <= 0:
                continue
            ranked.append(
                {
                    "event_id": event.get("event_id"),
                    "title": event.get("title"),
                    "date": event.get("date"),
                    "category": event.get("category"),
                    "similarity": similarity,
                    "returns": event.get("gold_returns_pct_vs_event_day", {}),
                    "short_term_bias": event.get("short_term_bias"),
                    "medium_term_bias": event.get("medium_term_bias"),
                    "long_term_bias": event.get("long_term_bias"),
                }
            )
        ranked.sort(key=lambda item: item["similarity"], reverse=True)
        matches.append(
            {
                "signal_title": signal.get("title"),
                "signal_category": signal.get("category"),
                "signal_direction": signal.get("direction"),
                "signal_intensity": signal.get("intensity"),
                "top_matches": ranked[:5],
                "aggregate_view": aggregate(ranked[:5]),
            }
        )

    write_json(
        PUBLIC_DATA / "similar_events.json",
        {
            "generated_at": utc_now_iso(),
            "data_quality": "token_similarity_mvp",
            "matches": matches,
        },
    )


def aggregate(matches: list[dict[str, object]]) -> dict[str, object]:
    horizons = ["1", "7", "30", "90", "180"]
    result: dict[str, object] = {}
    for horizon in horizons:
        values = []
        for match in matches:
            returns = match.get("returns", {}) or {}
            value = returns.get(horizon)
            if isinstance(value, (int, float)):
                values.append(float(value))
        if values:
            avg = sum(values) / len(values)
            result[f"avg_return_{horizon}d_pct"] = round(avg, 3)
            result[f"positive_share_{horizon}d"] = round(sum(1 for value in values if value > 0) / len(values), 3)
    return result


if __name__ == "__main__":
    main()
