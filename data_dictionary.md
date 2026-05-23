# Data Dictionary

## audience_segments.csv

- `audience_id`: Stable synthetic audience identifier.
- `audience_name`: Client-facing audience package name.
- `vertical`: Advertiser vertical.
- `sales_stage`: Pre-sales, post-sales, renewal, or expansion context.
- `client_type`: Modeled stakeholder type.
- `persona`: Plain-English audience definition.
- `primary_kpi`: KPI the package is intended to influence.
- `business_question`: Client question the package answers.
- `match_households_m`: Modeled matched households in millions.
- `match_rate_pct`: Modeled identity or match coverage.
- `topic_affinity_index`: Relative content and topic over-index.
- `action_propensity_index`: Modeled likelihood of downstream action.
- `ctv_index`, `linear_index`, `web_index`, `social_index`: Screen and channel behavior indices.
- `dma_lift_index`: Geographic concentration index.
- `daypart_fit_index`: Daypart suitability index.
- `measurement_confidence`: Readiness to defend measurement in a client conversation.
- `activation_readiness`: Readiness to move the insight into audience activation.
- `discovery_score`: Weighted package priority score.
- `package_recommendation`: Recommended package path and caveat.
- `narrative_headline`: Client-ready insight headline.
- `insight_summary`: Analyst narrative summary.

## Other Files

- `topic_affinity.csv`: Topic-level evidence for what the audience cares about.
- `dma_daypart_signals.csv`: Where and when planning evidence.
- `activation_plan.csv`: Activation tactics, surfaces, creative angles, confidence, effort, and owners.
- `qa_checks.csv`: Checks that prevent weak packages from being presented as fully ready.
- `package_sections.csv`: Presentation sections and analyst purpose statements.
