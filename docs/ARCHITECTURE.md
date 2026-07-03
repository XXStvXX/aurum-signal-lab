# Architecture

## Product Shape

Aurum Signal Lab is a research dashboard for gold event signals. It is not a generic price tracker. Its core loop is:

```text
Historical event -> event windows -> realized gold reaction
Live news -> event classification -> similar historical events -> model-ready signal
```

## Data Flow

```text
data/events/gold_events_seed.json
  -> scripts/event_study.py
  -> public/data/event_studies.json

GDELT Doc API
  -> scripts/signal_pipeline.py
  -> public/data/live_signals.json

event_studies + live_signals
  -> scripts/similarity.py
  -> public/data/similar_events.json

public/*.html/css/js
  -> GitHub Pages
```

## MVP Model Philosophy

The first prediction layer is evidence-based rather than black-box:

- classify the event type
- retrieve similar historical events
- summarize their realized outcomes
- estimate directional bias from historical analogues

The future trained model should consume features produced by the same pipeline:

- event category
- event intensity
- region
- source diversity
- GDELT tone
- historical similar-event returns
- pre-event gold momentum
- macro context: DXY, real yields, VIX, rates, inflation

## Production Upgrade Path

1. Replace rule-based classification with LLM JSON extraction.
2. Replace token similarity with `sentence-transformers` embeddings.
3. Store embeddings in Chroma or FAISS.
4. Train XGBoost models for `1d`, `1w`, `1m`, and `3m` labels.
5. Add macro data and out-of-sample backtests.
6. Record live predictions and score them after horizon expiry.
