# Attribution

This repository contains original code written for the Aurum Signal Lab MVP. No external project code has been copied into this repository.

The design borrows concepts, architecture ideas, and terminology from the following open-source projects and public documentation. Star counts were observed during research on 2026-07-03 and may change.

## Financial LLM And News Intelligence

- [AI4Finance-Foundation/FinGPT](https://github.com/AI4Finance-Foundation/FinGPT), MIT License, about 20.8k stars observed.
  - Inspiration: financial news sentiment, instruction tuning, FinGPT-Forecaster style workflow that combines ticker/date/news context with forecast output.
- [ProsusAI/finBERT](https://github.com/ProsusAI/finBERT), Apache-2.0 License, about 2.2k stars observed.
  - Inspiration: finance-domain sentiment classification and positive/neutral/negative scoring for financial text.

## Quant Research And Backtesting

- [microsoft/qlib](https://github.com/microsoft/qlib), MIT License, about 45.6k stars observed.
  - Inspiration: modular quant research pipeline: data, model training, backtesting, online analysis.
- [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB), AGPL-style open-source platform licensing should be checked before reuse, about 70k stars observed.
  - Inspiration: data platform pattern of connecting data once and consuming it through multiple analyst/agent surfaces.
- [polakowo/vectorbt](https://github.com/polakowo/vectorbt), Apache-2.0 License, high-star backtesting project.
  - Inspiration: matrix-oriented backtesting and fast experimentation mindset.

## Market Data And Indicators

- [ranaroussi/yfinance](https://github.com/ranaroussi/yfinance), Apache-2.0 License, high-star project.
  - Inspiration: simple research access to market data. This MVP does not import yfinance code.
- [TA-Lib/ta-lib-python](https://github.com/TA-Lib/ta-lib-python), BSD-style License.
  - Inspiration: mature technical indicator vocabulary. This MVP implements only simple returns and does not include TA-Lib code.

## News Collection

- [fhamborg/news-please](https://github.com/fhamborg/news-please), Apache-2.0 License, about 2.5k stars observed.
  - Inspiration: structured news extraction fields such as headline, lead, main text, image, author, publication date, and language.
- [codelucas/newspaper](https://github.com/codelucas/newspaper), mixed MIT/Apache licensing noted by the repository, high-star project.
  - Inspiration: lightweight article extraction and curation workflow.
- [alex9smith/gdelt-doc-api](https://github.com/alex9smith/gdelt-doc-api), MIT License.
  - Inspiration: Pythonic wrapper around GDELT 2.0 Doc API. This MVP calls GDELT directly with `urllib` instead of importing the library.
- [GDELT Project](https://www.gdeltproject.org/) and [GDELT 2.0 Doc API](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/).
  - Data-source inspiration for global public news monitoring.

## Similar Event Retrieval

- [huggingface/sentence-transformers](https://github.com/huggingface/sentence-transformers), Apache-2.0 License, about 18.9k stars observed.
  - Inspiration: semantic embeddings, retrieval, reranking, and future upgrade path for similar-event search.
- [chroma-core/chroma](https://github.com/chroma-core/chroma), Apache-2.0 License, about 28.7k stars observed.
  - Inspiration: local vector database pattern for AI retrieval.
- [facebookresearch/faiss](https://github.com/facebookresearch/faiss), MIT License, about 40.4k stars observed.
  - Inspiration: efficient similarity search for dense vectors.

## Modeling

- [dmlc/xgboost](https://github.com/dmlc/xgboost), Apache-2.0 License, about 28.5k stars observed.
  - Inspiration: gradient-boosted tree modeling for small/medium tabular data and interpretable feature importance.
- [lightgbm-org/LightGBM](https://github.com/lightgbm-org/LightGBM), MIT License.
  - Inspiration: fast boosted-tree classification and ranking.

## Event Study

- [LemaireJean-Baptiste/eventstudy](https://github.com/LemaireJean-Baptiste/eventstudy), GPL-3.0 License, about 68 stars observed.
  - Inspiration: financial event-study workflow for single events and event samples.
- [keysersoze23/event-study-toolkit](https://github.com/keysersoze23/event-study-toolkit), MIT License, about 5 stars observed.
  - Inspiration: abnormal returns, cumulative abnormal returns, and parametric/non-parametric event-study tests.

## GitHub Deployment

- [GitHub Pages documentation](https://docs.github.com/en/pages)
- [GitHub Actions scheduled workflows documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

These sources informed the GitHub Pages + scheduled Actions architecture. The implementation here is original.
