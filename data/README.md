# Data Sources

All data in this folder is deterministic synthetic data for a public adtech audience Discovery portfolio artifact. It does not represent any real advertiser, agency, publisher, platform, campaign, household, device, or customer record.

The generator uses seed `230523` and models the workflow structure of an audience insights analyst preparing client-facing Discovery packages. Public product research informed the structure of the workflow, but no proprietary platform data is used.

## Generated Files

- `audience_segments.csv`: 12 synthetic audience segments with business questions, KPIs, indices, confidence scores, and package recommendations.
- `topic_affinity.csv`: 60 modeled topic, keyword, and content-affinity signals.
- `dma_daypart_signals.csv`: 144 planning rows that connect DMA, daypart, lift indices, budget weights, and recommended channel paths.
- `activation_plan.csv`: 48 activation recommendations across contextual audiences, DSP paths, CTV tests, and measurement holdouts.
- `qa_checks.csv`: 60 package-readiness checks for audience definition, identity coverage, measurement, narrative, and activation.
- `package_sections.csv`: 60 client package sections that translate data into a presentation-ready story.

## Modeling Assumptions

- Audience indices are centered around 100, where values above 100 indicate over-indexing versus a generic baseline.
- Match scale is modeled in millions of households to reflect planning-level audience sizing, not person-level data.
- Discovery score is a transparent weighted score using topic affinity, action propensity, CTV index, web index, social index, match scale, measurement confidence, and activation readiness.
- Measurement confidence is reduced when match rate, event mapping, or activation readiness are weaker, so the artifact can show caveats before client presentation.
- DMA and daypart rows are generated from each audience's screen and content behavior so planning recommendations vary by audience rather than repeating one static dashboard.
