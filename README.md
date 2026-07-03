# Aurum Signal Lab

Gold news-event signal research platform for GitHub Pages.

This project studies how major news events affect gold across short, medium, and long horizons. It is designed around four layers:

1. Historical event library
2. Event-study engine for before/after gold returns
3. Live news signal extraction from public news feeds
4. Similar-event retrieval and model-ready prediction features

The first version is intentionally lightweight. It runs with Python's standard library, stores generated data as JSON, and serves a static dashboard from `public/`.

## Current MVP

- Curated seed library of gold-relevant historical events
- Event windows: `T-30`, `T-7`, `T`, `T+1`, `T+3`, `T+7`, `T+30`, `T+90`, `T+180`
- Live GDELT news fetch with rule-based event classification
- Similar-event matching based on token overlap
- GitHub Actions workflow for scheduled data refresh
- GitHub Pages workflow for static deployment
- Attribution notes for all project inspirations

## Run Locally

Generate data:

```bash
python3 scripts/event_study.py
python3 scripts/signal_pipeline.py
python3 scripts/similarity.py
```

Open:

```text
public/index.html
```

No build step is required.

## GitHub Deployment

1. Push these files to a GitHub repository.
2. In repository settings, enable GitHub Pages with GitHub Actions as the source.
3. The `pages.yml` workflow deploys `public/`.
4. The `data-refresh.yml` workflow refreshes JSON data on a schedule.

## Data Sources

The MVP uses:

- GDELT 2.0 Doc API for public news discovery
- Stooq daily CSV endpoint as a best-effort free gold price source
- Local deterministic fallback data so the dashboard remains testable offline

For production, replace or supplement with licensed gold spot, futures, real-yield, DXY, VIX, and rates data.

## Important

This is a research tool, not investment advice. The outputs are probabilistic research signals and historical analogies, not guaranteed forecasts.

## Sources And Inspirations

See `ATTRIBUTION.md`.
