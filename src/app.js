const state = {
  selectedId: null,
};

const byId = (id) => document.getElementById(id);
const money = (value) => `${Number(value).toFixed(1)}M`;
const rounded = (value) => Number(value).toFixed(0);

function sortedAudiences() {
  return [...discoveryData.audiences].sort((a, b) => b.discovery_score - a.discovery_score);
}

function selectedAudience() {
  return discoveryData.audiences.find((audience) => audience.audience_id === state.selectedId) || sortedAudiences()[0];
}

function recommendationClass(recommendation) {
  if (recommendation === "Lead package") return "lead";
  if (recommendation.includes("caveat")) return "watch";
  return "";
}

function setMetrics() {
  const audiences = discoveryData.audiences;
  const households = audiences.reduce((sum, row) => sum + row.match_households_m, 0);
  const confidence = audiences.reduce((sum, row) => sum + row.measurement_confidence, 0) / audiences.length;
  const ready = audiences.filter((row) => row.package_recommendation === "Lead package").length;
  byId("metric-audiences").textContent = audiences.length;
  byId("metric-households").textContent = money(households);
  byId("metric-confidence").textContent = rounded(confidence);
  byId("metric-ready").textContent = ready;
}

function renderQueue() {
  const body = byId("queue-body");
  body.innerHTML = sortedAudiences().map((audience, index) => `
    <tr class="${audience.audience_id === state.selectedId ? "is-selected" : ""}" data-audience-id="${audience.audience_id}">
      <td>${index + 1}</td>
      <td>
        <span class="audience-name">${audience.audience_name}</span>
        <span class="muted">${audience.vertical} | ${audience.primary_kpi}</span>
      </td>
      <td>${audience.sales_stage}</td>
      <td><span class="score-pill">${audience.discovery_score}</span></td>
      <td><span class="status-pill ${recommendationClass(audience.package_recommendation)}">${audience.package_recommendation}</span></td>
    </tr>
  `).join("");

  body.querySelectorAll("tr").forEach((row) => {
    row.addEventListener("click", () => {
      state.selectedId = row.dataset.audienceId;
      renderAll();
    });
  });

  renderQueueDetail();
}

function renderQueueDetail() {
  const audience = selectedAudience();
  byId("queue-detail").innerHTML = `
    <p class="eyebrow">Selected package</p>
    <h3 class="detail-title">${audience.audience_name}</h3>
    <p class="insight-copy">${audience.narrative_headline}</p>
    <div class="detail-kpis">
      ${miniMetric("Matched households", money(audience.match_households_m))}
      ${miniMetric("Action propensity", audience.action_propensity_index)}
      ${miniMetric("Measurement confidence", audience.measurement_confidence)}
      ${miniMetric("Activation readiness", audience.activation_readiness)}
    </div>
    <p class="insight-copy"><strong>Client question:</strong> ${audience.business_question}</p>
    <p class="insight-copy"><strong>Recommended package path:</strong> ${audience.package_recommendation}.</p>
  `;
}

function miniMetric(label, value) {
  return `
    <div class="mini-metric">
      <span>${label}</span>
      <strong>${value}</strong>
    </div>
  `;
}

function renderSelect() {
  const select = byId("audience-select");
  select.innerHTML = sortedAudiences().map((audience) => `
    <option value="${audience.audience_id}" ${audience.audience_id === state.selectedId ? "selected" : ""}>
      ${audience.audience_name}
    </option>
  `).join("");

  select.onchange = (event) => {
    state.selectedId = event.target.value;
    renderAll();
  };
}

function renderStory() {
  const audience = selectedAudience();
  byId("story-card").innerHTML = `
    <p class="eyebrow">${audience.sales_stage}</p>
    <h3>${audience.audience_name}</h3>
    <p class="story-question">${audience.business_question}</p>
    <p class="insight-copy">${audience.insight_summary}</p>
    <div class="story-metrics">
      ${miniMetric("CTV index", audience.ctv_index)}
      ${miniMetric("Web index", audience.web_index)}
      ${miniMetric("Social index", audience.social_index)}
      ${miniMetric("DMA lift", audience.dma_lift_index)}
    </div>
    <p class="insight-copy"><strong>Audience definition:</strong> ${audience.persona}</p>
  `;

  const topics = discoveryData.topics
    .filter((topic) => topic.audience_id === audience.audience_id)
    .sort((a, b) => b.affinity_index - a.affinity_index);

  byId("topic-bars").innerHTML = topics.map((topic) => {
    const width = Math.min(100, Math.max(24, (topic.affinity_index / 165) * 100));
    return `
      <div class="bar-row">
        <div class="bar-label"><span>${topic.topic}</span><span>${topic.affinity_index}</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div>
        <span class="muted">${topic.evidence_signal} | ${topic.topic_type}</span>
      </div>
    `;
  }).join("");

  const dmas = discoveryData.dmaSignals
    .filter((signal) => signal.audience_id === audience.audience_id)
    .sort((a, b) => b.budget_weight - a.budget_weight)
    .slice(0, 6);

  byId("dma-grid").innerHTML = dmas.map((signal) => `
    <div class="dma-card">
      <strong>${signal.dma}</strong>
      <span>${signal.daypart}</span>
      <span>CTV ${signal.ctv_lift_index} | Web ${signal.web_lift_index}</span>
      <span>${signal.recommended_channel}</span>
    </div>
  `).join("");
}

function renderActivation() {
  const audience = selectedAudience();
  const actions = discoveryData.activationPlan.filter((row) => row.audience_id === audience.audience_id);
  byId("activation-list").innerHTML = actions.map((action) => `
    <div class="action-card">
      <strong>${action.tactic}</strong>
      <p>${action.creative_angle}</p>
      <div class="qa-meta">
        <span>${action.surface}</span>
        <span>${action.expected_lift_pct}% modeled lift</span>
        <span>${action.confidence} confidence</span>
      </div>
    </div>
  `).join("");

  const checks = discoveryData.qaChecks.filter((row) => row.audience_id === audience.audience_id);
  byId("qa-list").innerHTML = checks.map((check) => `
    <div class="qa-card">
      <strong>${check.check_name}</strong>
      <p>${check.remediation}</p>
      <div class="qa-meta">
        <span>${check.check_area}</span>
        <span>${check.status}</span>
        <span>${check.owner}</span>
      </div>
    </div>
  `).join("");

  const sections = discoveryData.packageSections
    .filter((section) => section.audience_id === audience.audience_id)
    .sort((a, b) => a.section_order - b.section_order);

  byId("package-flow").innerHTML = sections.map((section) => `
    <li><strong>${section.section_name}:</strong> ${section.detail}. ${section.analyst_purpose}</li>
  `).join("");
}

function setupTabs() {
  document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => {
      activateTab(button.dataset.tab);
      const url = new URL(window.location.href);
      url.searchParams.set("surface", button.dataset.tab);
      window.history.replaceState(null, "", url);
    });
  });
}

function activateTab(tabId) {
  const fallback = byId(tabId) ? tabId : "queue";
  document.querySelectorAll(".tab").forEach((tabButton) => {
    tabButton.classList.toggle("is-active", tabButton.dataset.tab === fallback);
  });
  document.querySelectorAll(".surface").forEach((surface) => {
    surface.classList.toggle("is-active", surface.id === fallback);
  });
}

function renderAll() {
  if (!state.selectedId) {
    state.selectedId = sortedAudiences()[0].audience_id;
  }
  setMetrics();
  renderQueue();
  renderSelect();
  renderStory();
  renderActivation();
}

setupTabs();
renderAll();
activateTab(new URLSearchParams(window.location.search).get("surface") || "queue");
