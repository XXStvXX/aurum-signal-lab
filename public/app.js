const paths = {
  studies: "./data/event_studies.json",
  signals: "./data/live_signals.json",
  matches: "./data/similar_events.json",
};

const state = {
  studies: null,
  signals: null,
  matches: null,
  category: "all",
};

const formatReturn = (value) => {
  if (typeof value !== "number") return "-";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
};

const formatTime = (value) => {
  if (!value) return "-";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
};

async function loadJson(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`Failed to fetch ${path}`);
  return response.json();
}

async function boot() {
  const status = document.querySelector("#status");
  try {
    const [studies, signals, matches] = await Promise.all([
      loadJson(paths.studies),
      loadJson(paths.signals),
      loadJson(paths.matches),
    ]);
    state.studies = studies;
    state.signals = signals;
    state.matches = matches;
    status.textContent = "Data loaded";
    status.dataset.kind = "ok";
    render();
  } catch (error) {
    status.textContent = "Data unavailable";
    status.dataset.kind = "bad";
    console.error(error);
  }
}

function render() {
  renderSummary();
  renderCategoryFilter();
  renderSignals();
  renderMatches();
  renderEventTable();
}

function renderSummary() {
  document.querySelector("#eventCount").textContent = state.studies?.events?.length ?? 0;
  document.querySelector("#signalCount").textContent = state.signals?.signals?.length ?? 0;
  document.querySelector("#matchCount").textContent = state.matches?.matches?.length ?? 0;
  document.querySelector("#refreshTime").textContent = formatTime(state.signals?.generated_at || state.studies?.generated_at);
  document.querySelector("#studyQuality").textContent = state.studies?.data_quality || "";
  document.querySelector("#similarityQuality").textContent = state.matches?.data_quality || "";
}

function renderCategoryFilter() {
  const select = document.querySelector("#categoryFilter");
  const categories = [...new Set((state.signals?.signals || []).map((item) => item.category).filter(Boolean))].sort();
  const current = select.value || "all";
  select.innerHTML = `<option value="all">All categories</option>${categories
    .map((category) => `<option value="${category}">${category.replaceAll("_", " ")}</option>`)
    .join("")}`;
  select.value = categories.includes(current) ? current : "all";
  state.category = select.value;
  select.onchange = () => {
    state.category = select.value;
    renderSignals();
  };
}

function filteredSignals() {
  const signals = state.signals?.signals || [];
  if (state.category === "all") return signals;
  return signals.filter((signal) => signal.category === state.category);
}

function renderSignals() {
  const container = document.querySelector("#signals");
  const signals = filteredSignals();
  if (!signals.length) {
    container.innerHTML = `<p class="empty">No signals available.</p>`;
    return;
  }
  container.innerHTML = signals
    .map(
      (signal) => `
      <article class="signal-card">
        <div class="signal-main">
          <span class="badge">${signal.category?.replaceAll("_", " ") || "unclassified"}</span>
          <h3>${escapeHtml(signal.title)}</h3>
          <p>${signal.domain || "unknown source"} · ${signal.source_country || "unknown region"} · ${signal.seen_at || "no timestamp"}</p>
        </div>
        <div class="signal-score">
          <strong>${signal.intensity ?? "-"}</strong>
          <span>${signal.direction?.replaceAll("_", " ") || "watch"}</span>
        </div>
      </article>
    `,
    )
    .join("");
}

function renderMatches() {
  const container = document.querySelector("#matches");
  const matches = state.matches?.matches || [];
  if (!matches.length) {
    container.innerHTML = `<p class="empty">No similar-event matches yet.</p>`;
    return;
  }
  container.innerHTML = matches
    .slice(0, 8)
    .map((match) => {
      const aggregate = match.aggregate_view || {};
      const top = match.top_matches || [];
      return `
        <article class="match-card">
          <div>
            <span class="badge">${match.signal_category?.replaceAll("_", " ") || "signal"}</span>
            <h3>${escapeHtml(match.signal_title || "")}</h3>
            <div class="horizon-row">
              <span>1w avg ${formatReturn(aggregate.avg_return_7d_pct)}</span>
              <span>1m avg ${formatReturn(aggregate.avg_return_30d_pct)}</span>
              <span>6m avg ${formatReturn(aggregate.avg_return_180d_pct)}</span>
            </div>
          </div>
          <ol>
            ${top
              .map(
                (event) => `
                <li>
                  <strong>${escapeHtml(event.title || "")}</strong>
                  <span>${event.date} · ${(event.similarity * 100).toFixed(1)}% similar · T+30 ${formatReturn(event.returns?.["30"])}</span>
                </li>
              `,
              )
              .join("")}
          </ol>
        </article>
      `;
    })
    .join("");
}

function renderEventTable() {
  const body = document.querySelector("#eventTable");
  const events = state.studies?.events || [];
  body.innerHTML = events
    .map(
      (event) => `
      <tr>
        <td>
          <strong>${escapeHtml(event.title)}</strong>
          <span>${event.date} · ${event.region}</span>
        </td>
        <td>${event.category?.replaceAll("_", " ")}</td>
        <td>${formatReturn(event.gold_returns_pct_vs_event_day?.["7"])}</td>
        <td>${formatReturn(event.gold_returns_pct_vs_event_day?.["30"])}</td>
        <td>${formatReturn(event.gold_returns_pct_vs_event_day?.["180"])}</td>
      </tr>
    `,
    )
    .join("");
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

boot();
