# Event Schema

Historical event records live in `data/events/gold_events_seed.json`.

```json
{
  "event_id": "svb-collapse-2023",
  "date": "2023-03-10",
  "title": "Silicon Valley Bank collapse",
  "category": "banking_crisis",
  "region": "US",
  "summary": "Silicon Valley Bank failed, triggering stress across US regional banks.",
  "expected_gold_channel": [
    "safe_haven",
    "rate_cut_expectations",
    "financial_stability"
  ]
}
```

## Categories

- `fed_policy`
- `war`
- `geopolitical_shock`
- `financial_crisis`
- `banking_crisis`
- `inflation`
- `sovereign_debt`
- `usd_rates`
- `central_bank_gold`
- `political_shock`
- `market_news`

## Generated Fields

`scripts/event_study.py` adds:

- `price_observations`
- `gold_returns_pct_vs_event_day`
- `short_term_bias`
- `medium_term_bias`
- `long_term_bias`

## Required Improvement Before Production

Each curated event should eventually include source URLs, a primary timestamp, market-session context, and whether the event was anticipated or surprising.
