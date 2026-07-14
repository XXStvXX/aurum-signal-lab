# Aurum Signal Lab

A research prototype for studying how major news events relate to gold returns across short, medium, and long horizons.

- [Live dashboard](https://xxstvxx.github.io/aurum-signal-lab/)
- [Repository](https://github.com/XXStvXX/aurum-signal-lab)

The project connects four layers:

1. a curated historical event library
2. an event-study engine for before/after gold returns
3. public-news signal extraction
4. similar-event retrieval for research context

It is designed as an explainable portfolio project, not a trading system. The dashboard makes data provenance and offline fallback states visible so a reviewer can distinguish live inputs from demonstration data.

## What the Dashboard Shows

- Historical gold-relevant events grouped by category
- Event windows from `T-30` through `T+180`
- Live or fallback news signals with category and directional labels
- Similar historical events based on token overlap
- Average post-event returns across multiple horizons
- Refresh status and data-source state

## Live Demo Notes

The GitHub Pages dashboard is intentionally static and lightweight. Generated JSON is served from `public/`, so no backend is required.

When external feeds are unavailable, the pipeline uses deterministic offline fallback data. The dashboard labels that state explicitly. Fallback results demonstrate the workflow and interface; they should not be interpreted as current market signals.

## Methodology

### Event study

For each curated event, the pipeline compares gold prices around the event date using these windows:

`T-30`, `T-7`, `T`, `T+1`, `T+3`, `T+7`, `T+30`, `T+90`, and `T+180`.

Returns are descriptive historical observations. They do not establish that the event caused the price movement.

### News classification

Public news records are categorized with transparent rules for themes such as:

- Federal Reserve policy
- war and geopolitical shocks
- banking or liquidity stress
- sovereign debt
- inflation and macroeconomic releases

### Similar-event retrieval

The MVP ranks historical analogues using token overlap. This is deliberately interpretable, but limited: shared words do not guarantee equivalent economic conditions.

## Current MVP

- Curated seed library of 19 gold-relevant historical events
- Event-study generation across nine time windows
- GDELT news fetch with rule-based classification
- Similar-event matching based on token overlap
- Static GitHub Pages dashboard
- Scheduled GitHub Actions data refresh
- Deterministic fallback data for offline testing
- Source and inspiration notes in [`ATTRIBUTION.md`](ATTRIBUTION.md)

## Run Locally

Generate the project data:

```bash
python3 scripts/event_study.py
python3 scripts/signal_pipeline.py
python3 scripts/similarity.py
```

Then open:

```text
public/index.html
```

No package installation or build step is required for the current standard-library MVP.

## Repository Structure

```text
.
├── data/                  # Curated inputs and generated research data
├── public/                # Static dashboard and generated JSON
├── scripts/
│   ├── event_study.py     # Historical return-window generation
│   ├── signal_pipeline.py # News collection and classification
│   └── similarity.py      # Historical analogue matching
├── .github/workflows/     # Pages deployment and scheduled refresh
└── ATTRIBUTION.md         # Data-source and inspiration notes
```

## Data Sources

The MVP uses:

- GDELT 2.0 Doc API for public news discovery
- Stooq daily CSV endpoint as a best-effort free gold-price source
- local deterministic fallback data so the dashboard remains testable offline

A production-grade version would require licensed, quality-controlled market data and additional explanatory variables such as real yields, DXY, VIX, rates, and liquidity conditions.

## AI-Assisted Workflow

AI supported requirements clarification, implementation planning, documentation, and iterative debugging. Final scope decisions, source selection, interpretation, limitation statements, and published claims are reviewed by the project owner.

This is a human-in-the-loop research workflow: AI accelerates delivery, while responsibility for validation and communication remains with the human operator.

## Limitations

- The historical event library is curated and small.
- Token overlap is a baseline similarity method, not semantic or causal matching.
- Event windows may contain many overlapping market drivers.
- Free public endpoints can be delayed, unavailable, or revised.
- Offline fallback data is for interface and pipeline testing only.
- Historical analogues do not predict future returns.

## Roadmap

- Validate event dates and price observations with stronger source controls
- Add real-yield, DXY, VIX, and rate-change context
- Replace token overlap with an evaluated semantic-retrieval baseline
- Add automated data-quality checks and test coverage
- Separate live, stale, and fallback data more prominently in generated outputs

## Disclaimer

This project is for education and research. It is not investment advice, and its outputs are not trading recommendations.
