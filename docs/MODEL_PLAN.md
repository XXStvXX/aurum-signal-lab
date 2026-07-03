# Model Plan

## First Trainable Target

Train separate classifiers for these labels:

- `gold_up_1d`
- `gold_up_7d`
- `gold_up_30d`
- `gold_up_90d`

Each label is true when realized gold return is above zero at that horizon.

## Feature Groups

Historical event features:

- `category`
- `region`
- `expected_gold_channel`
- historical similar-event average returns
- historical similar-event positive share

Live news features:

- headline category
- rule or LLM intensity score
- source country
- source domain count by event cluster
- GDELT tone and volume if available

Market features:

- gold return over prior 1, 7, 30 days
- DXY return over prior 1, 7, 30 days
- 10Y nominal yield change
- 10Y real yield change
- VIX level and change

## Recommended Baseline

Start with logistic regression and XGBoost. Avoid fine-tuning a large language model until the dataset has enough high-quality labels.

## Evaluation

- Use walk-forward validation.
- Keep a strict out-of-sample period.
- Score direction accuracy, precision for bullish calls, recall for major upside moves, and calibration.
- Track every live prediction and score it after the horizon expires.

## Why Not Train Immediately?

The current seed library is too small. A serious first model needs at least hundreds of labeled events and thousands of clustered news observations. Until then, similar-event retrieval is more transparent and less likely to overfit.
