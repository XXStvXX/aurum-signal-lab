from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

from common import PUBLIC_DATA, classify_event, utc_now_iso, write_json


GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"


def fetch_gdelt() -> list[dict[str, object]]:
    query = '("gold" OR "XAU" OR "bullion") ("Federal Reserve" OR war OR inflation OR dollar OR yields OR "central bank" OR banking)'
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": "50",
        "sort": "hybridrel",
    }
    url = f"{GDELT_ENDPOINT}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []
    return payload.get("articles", []) or []


def fallback_articles() -> list[dict[str, object]]:
    return [
        {
            "title": "Gold traders watch Federal Reserve rate outlook as dollar yields rise",
            "url": "https://example.com/fallback-fed-gold",
            "domain": "example.com",
            "seendate": "offline",
            "language": "English",
            "sourcecountry": "US",
        },
        {
            "title": "Middle East escalation keeps safe-haven demand for bullion in focus",
            "url": "https://example.com/fallback-war-gold",
            "domain": "example.com",
            "seendate": "offline",
            "language": "English",
            "sourcecountry": "US",
        },
        {
            "title": "Banking sector stress revives discussion of liquidity and gold hedges",
            "url": "https://example.com/fallback-bank-gold",
            "domain": "example.com",
            "seendate": "offline",
            "language": "English",
            "sourcecountry": "US",
        },
    ]


def normalize_article(article: dict[str, object]) -> dict[str, object]:
    title = str(article.get("title") or "").strip()
    analysis = classify_event(title)
    return {
        "title": title,
        "url": article.get("url"),
        "domain": article.get("domain"),
        "seen_at": article.get("seendate"),
        "language": article.get("language"),
        "source_country": article.get("sourcecountry"),
        "category": analysis["category"],
        "direction": analysis["direction"],
        "intensity": analysis["intensity"],
        "matched_terms": analysis["matched_terms"],
    }


def main() -> None:
    articles = fetch_gdelt()
    data_quality = "gdelt_doc_api" if articles else "offline_fallback_articles"
    if not articles:
        articles = fallback_articles()
    signals = [normalize_article(article) for article in articles if str(article.get("title") or "").strip()]
    payload = {
        "generated_at": utc_now_iso(),
        "data_quality": data_quality,
        "signals": signals[:30],
    }
    write_json(PUBLIC_DATA / "live_signals.json", payload)


if __name__ == "__main__":
    main()
