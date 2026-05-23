import csv
import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
OUTPUTS = ANALYSIS / "outputs"
SRC = ROOT / "src"
SEED = 230523


AUDIENCES = [
    {
        "id": "AUD-STREAM-01",
        "name": "Premium Streaming Switchers",
        "vertical": "Entertainment",
        "stage": "Pre-sales RFP",
        "client_type": "Agency holding company",
        "persona": "Households comparing premium streaming bundles",
        "kpi": "trial starts",
        "question": "Where should a streaming brand find likely switchers without overbuying the same CTV viewers?",
        "headline": "Streaming switchers over-index on review content, late evening CTV, and mobile sign-up research.",
        "base_scale": 7.4,
        "base_propensity": 122,
        "ctv": 139,
        "linear": 94,
        "web": 128,
        "social": 118,
        "topics": ["bundle comparisons", "prestige dramas", "sports streaming", "device setup", "family plans"],
        "dmas": ["Los Angeles", "Chicago", "Dallas-Fort Worth", "Atlanta"],
        "dayparts": ["Late evening", "Prime access", "Weekend afternoon"],
    },
    {
        "id": "AUD-QSR-02",
        "name": "Value QSR Occasion Builders",
        "vertical": "Restaurants",
        "stage": "Post-sales optimization",
        "client_type": "National brand",
        "persona": "Families and commuters choosing quick meals by price, route, and time of day",
        "kpi": "store visits",
        "question": "Which consumption windows and local signals should guide value-menu creative rotation?",
        "headline": "Value dining demand clusters around commute and weekend errand windows with strong local offer sensitivity.",
        "base_scale": 8.8,
        "base_propensity": 116,
        "ctv": 112,
        "linear": 106,
        "web": 119,
        "social": 130,
        "topics": ["value menus", "drive-through speed", "kids meals", "mobile coupons", "late-night snacks"],
        "dmas": ["Houston", "Phoenix", "Tampa", "Detroit"],
        "dayparts": ["Morning commute", "Lunch", "Late night"],
    },
    {
        "id": "AUD-AUTO-03",
        "name": "EV Curious Auto Intenders",
        "vertical": "Automotive",
        "stage": "Pre-sales strategy",
        "client_type": "OEM media team",
        "persona": "In-market buyers comparing hybrid, EV, and charging cost tradeoffs",
        "kpi": "dealer lead submissions",
        "question": "How should an EV launch separate curiosity from high-intent research?",
        "headline": "High-intent EV audiences show stronger charging, tax-credit, and local inventory signals than broad green topics.",
        "base_scale": 5.9,
        "base_propensity": 135,
        "ctv": 123,
        "linear": 87,
        "web": 145,
        "social": 113,
        "topics": ["charging maps", "tax credits", "range anxiety", "lease calculators", "local inventory"],
        "dmas": ["San Francisco-Oakland-San Jose", "Seattle-Tacoma", "Denver", "Boston"],
        "dayparts": ["Early evening", "Weekend afternoon", "Late evening"],
    },
    {
        "id": "AUD-TRAVEL-04",
        "name": "Family Vacation Planners",
        "vertical": "Travel",
        "stage": "Pre-sales RFP",
        "client_type": "Travel marketplace",
        "persona": "Parents balancing school calendars, deal windows, and destination research",
        "kpi": "booking starts",
        "question": "Which audience story supports a seasonal family travel package before peak planning closes?",
        "headline": "Family planners move from inspiration to price checks quickly, especially in school-break feeder markets.",
        "base_scale": 7.1,
        "base_propensity": 128,
        "ctv": 118,
        "linear": 101,
        "web": 136,
        "social": 126,
        "topics": ["school breaks", "hotel pools", "flight deals", "theme parks", "travel insurance"],
        "dmas": ["New York", "Orlando-Daytona Beach-Melbourne", "Philadelphia", "Minneapolis-St. Paul"],
        "dayparts": ["Weekend morning", "Prime access", "Late evening"],
    },
    {
        "id": "AUD-FIN-05",
        "name": "Cash-Flow Conscious Borrowers",
        "vertical": "Financial services",
        "stage": "Post-sales expansion",
        "client_type": "Fintech growth team",
        "persona": "Consumers researching debt consolidation, credit score movement, and monthly payment relief",
        "kpi": "qualified applications",
        "question": "Which segments are ready for education-led acquisition rather than rate-only messaging?",
        "headline": "Borrower intent is strongest where credit education and monthly payment calculators appear together.",
        "base_scale": 6.4,
        "base_propensity": 132,
        "ctv": 107,
        "linear": 92,
        "web": 147,
        "social": 121,
        "topics": ["credit score tips", "payment calculators", "debt consolidation", "APR explainers", "budget apps"],
        "dmas": ["Charlotte", "Atlanta", "Las Vegas", "Cleveland-Akron"],
        "dayparts": ["Early evening", "Late evening", "Weekend afternoon"],
    },
    {
        "id": "AUD-HEALTH-06",
        "name": "Active Wellness Routine Builders",
        "vertical": "Health and fitness",
        "stage": "Client renewal",
        "client_type": "Retail media advertiser",
        "persona": "Adults building routines around fitness, supplements, sleep, and meal planning",
        "kpi": "retail conversions",
        "question": "Which wellness motivations should shape the next creative and contextual audience test?",
        "headline": "Routine builders respond to goal-based content more than generic fitness reach.",
        "base_scale": 6.8,
        "base_propensity": 119,
        "ctv": 116,
        "linear": 89,
        "web": 130,
        "social": 137,
        "topics": ["sleep quality", "strength training", "protein snacks", "habit tracking", "meal prep"],
        "dmas": ["Austin", "San Diego", "Portland", "Raleigh-Durham"],
        "dayparts": ["Morning commute", "Early evening", "Weekend morning"],
    },
    {
        "id": "AUD-RETAIL-07",
        "name": "Deal-Led Omnichannel Shoppers",
        "vertical": "Retail",
        "stage": "Pre-sales strategy",
        "client_type": "Big-box retailer",
        "persona": "Shoppers comparing circulars, social deal content, pickup options, and loyalty offers",
        "kpi": "incremental store and site actions",
        "question": "How can a retail advertiser connect deal intent to channel and creative choices?",
        "headline": "Deal-led shoppers need a cross-device plan because discovery happens socially and conversion often moves to web or store.",
        "base_scale": 9.2,
        "base_propensity": 114,
        "ctv": 110,
        "linear": 104,
        "web": 126,
        "social": 142,
        "topics": ["weekly circulars", "pickup windows", "loyalty rewards", "price matching", "social hauls"],
        "dmas": ["Dallas-Fort Worth", "Nashville", "Kansas City", "Columbus"],
        "dayparts": ["Lunch", "Prime access", "Weekend morning"],
    },
    {
        "id": "AUD-HOME-08",
        "name": "Home Project Researchers",
        "vertical": "Home improvement",
        "stage": "Post-sales optimization",
        "client_type": "Retail and services brand",
        "persona": "Homeowners researching project difficulty, contractor cost, and seasonal timing",
        "kpi": "quote requests",
        "question": "Which project signals should split DIY education from pro-service lead generation?",
        "headline": "Project researchers move from inspiration to quote behavior when cost, weather, and difficulty content align.",
        "base_scale": 6.1,
        "base_propensity": 126,
        "ctv": 121,
        "linear": 99,
        "web": 141,
        "social": 115,
        "topics": ["kitchen refresh", "contractor cost", "paint trends", "storm prep", "tool rentals"],
        "dmas": ["Miami-Fort Lauderdale", "Houston", "St. Louis", "Sacramento"],
        "dayparts": ["Weekend morning", "Weekend afternoon", "Early evening"],
    },
    {
        "id": "AUD-B2B-09",
        "name": "Small Business Software Evaluators",
        "vertical": "B2B software",
        "stage": "Pre-sales RFP",
        "client_type": "SaaS demand generation",
        "persona": "Operators comparing automation, invoicing, workflow, and analytics tools",
        "kpi": "demo requests",
        "question": "Which business-owner signals are specific enough to support a targeted CTV plus digital plan?",
        "headline": "Software evaluators cluster around workflow pain and peer proof, not broad entrepreneurship content.",
        "base_scale": 4.7,
        "base_propensity": 131,
        "ctv": 103,
        "linear": 76,
        "web": 149,
        "social": 118,
        "topics": ["workflow automation", "invoice software", "cash flow", "customer follow-up", "review sites"],
        "dmas": ["San Francisco-Oakland-San Jose", "Austin", "Seattle-Tacoma", "New York"],
        "dayparts": ["Morning commute", "Lunch", "Early evening"],
    },
    {
        "id": "AUD-SPORTS-10",
        "name": "Live Sports Streaming Fans",
        "vertical": "Media and sports",
        "stage": "Client renewal",
        "client_type": "Sports media seller",
        "persona": "Fans mixing linear games, highlights, fantasy research, and social clips",
        "kpi": "subscription and tune-in actions",
        "question": "How should a sports package prove incremental reach across linear and streaming?",
        "headline": "Sports fans show a measurable bridge from linear tune-in to streaming highlights and mobile companion behavior.",
        "base_scale": 8.1,
        "base_propensity": 123,
        "ctv": 146,
        "linear": 133,
        "web": 124,
        "social": 139,
        "topics": ["fantasy matchups", "live scores", "sports documentaries", "team podcasts", "betting odds"],
        "dmas": ["Boston", "Philadelphia", "Chicago", "Phoenix"],
        "dayparts": ["Prime access", "Late evening", "Weekend afternoon"],
    },
    {
        "id": "AUD-CPG-11",
        "name": "Better-For-You Grocery Explorers",
        "vertical": "CPG",
        "stage": "Post-sales expansion",
        "client_type": "Consumer brand",
        "persona": "Shoppers evaluating ingredients, recipes, dietary swaps, and retailer availability",
        "kpi": "retail actions",
        "question": "Which content affinities should inform audience, retail media, and creative messaging?",
        "headline": "Ingredient curiosity becomes purchase intent when recipe content and local availability are both present.",
        "base_scale": 7.7,
        "base_propensity": 118,
        "ctv": 109,
        "linear": 97,
        "web": 132,
        "social": 144,
        "topics": ["ingredient labels", "healthy swaps", "recipe videos", "grocery pickup", "family snacks"],
        "dmas": ["Portland", "Denver", "Minneapolis-St. Paul", "Raleigh-Durham"],
        "dayparts": ["Weekend morning", "Lunch", "Early evening"],
    },
    {
        "id": "AUD-LUX-12",
        "name": "Aspirational Luxury Researchers",
        "vertical": "Luxury retail",
        "stage": "Pre-sales strategy",
        "client_type": "Premium retail brand",
        "persona": "Shoppers researching investment pieces, creator reviews, resale value, and gifting moments",
        "kpi": "high-value site actions",
        "question": "How can premium creative reach high-intent researchers without diluting brand context?",
        "headline": "Luxury researchers need curated context, premium CTV adjacency, and high-confidence measurement before scale.",
        "base_scale": 3.9,
        "base_propensity": 136,
        "ctv": 117,
        "linear": 82,
        "web": 151,
        "social": 127,
        "topics": ["investment pieces", "gift guides", "resale value", "designer profiles", "creator reviews"],
        "dmas": ["New York", "Los Angeles", "Miami-Fort Lauderdale", "San Francisco-Oakland-San Jose"],
        "dayparts": ["Late evening", "Weekend afternoon", "Prime access"],
    },
]


def clamp(value, low, high):
    return max(low, min(high, value))


def weighted_score(row):
    scale_component = min(row["match_households_m"] / 9.5, 1) * 100
    return round(
        0.19 * row["topic_affinity_index"]
        + 0.15 * row["action_propensity_index"]
        + 0.13 * row["ctv_index"]
        + 0.10 * row["web_index"]
        + 0.07 * row["social_index"]
        + 0.12 * scale_component
        + 0.12 * row["measurement_confidence"]
        + 0.12 * row["activation_readiness"],
        1,
    )


def package_recommendation(score, confidence, readiness):
    if score >= 111 and confidence >= 76 and readiness >= 76:
        return "Lead package"
    if confidence < 70:
        return "Insight package with measurement caveat"
    if readiness < 70:
        return "Audience story plus activation prep"
    return "Test package"


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_rows():
    random.seed(SEED)
    audience_rows = []
    topic_rows = []
    dma_rows = []
    activation_rows = []
    qa_rows = []
    package_rows = []

    for item in AUDIENCES:
        noise = random.Random(SEED + len(item["id"]))
        match_households_m = round(clamp(item["base_scale"] + noise.uniform(-0.45, 0.55), 2.8, 9.8), 2)
        match_rate_pct = round(clamp(18 + match_households_m * 3.8 + noise.uniform(-4, 4), 20, 58), 1)
        topic_affinity = round(clamp(sum([118 + i * 4 for i, _ in enumerate(item["topics"])]) / 5 + noise.uniform(-6, 8), 105, 154), 1)
        dma_lift = round(clamp(111 + match_households_m * 3 + noise.uniform(-5, 10), 104, 146), 1)
        daypart_fit = round(clamp((item["ctv"] * 0.45 + item["web"] * 0.30 + item["social"] * 0.25) + noise.uniform(-7, 7), 94, 153), 1)
        measurement_confidence = round(clamp(62 + match_rate_pct * 0.34 + item["web"] * 0.08 + noise.uniform(-8, 7), 58, 93), 1)
        activation_readiness = round(clamp(54 + item["ctv"] * 0.13 + item["social"] * 0.09 + match_households_m * 2.2 + noise.uniform(-6, 7), 55, 94), 1)

        row = {
            "audience_id": item["id"],
            "audience_name": item["name"],
            "vertical": item["vertical"],
            "sales_stage": item["stage"],
            "client_type": item["client_type"],
            "persona": item["persona"],
            "primary_kpi": item["kpi"],
            "business_question": item["question"],
            "match_households_m": match_households_m,
            "match_rate_pct": match_rate_pct,
            "topic_affinity_index": topic_affinity,
            "action_propensity_index": item["base_propensity"],
            "ctv_index": item["ctv"],
            "linear_index": item["linear"],
            "web_index": item["web"],
            "social_index": item["social"],
            "dma_lift_index": dma_lift,
            "daypart_fit_index": daypart_fit,
            "measurement_confidence": measurement_confidence,
            "activation_readiness": activation_readiness,
            "discovery_score": 0,
            "package_recommendation": "",
            "narrative_headline": item["headline"],
            "insight_summary": f"{item['persona']} show a defendable path from content interest to {item['kpi']} when the package connects topic, screen, place, and measurement evidence.",
        }
        row["discovery_score"] = weighted_score(row)
        row["package_recommendation"] = package_recommendation(
            row["discovery_score"],
            row["measurement_confidence"],
            row["activation_readiness"],
        )
        audience_rows.append(row)

        for idx, topic in enumerate(item["topics"]):
            affinity = round(clamp(topic_affinity + 11 - idx * 4 + noise.uniform(-5, 5), 95, 165), 1)
            topic_rows.append(
                {
                    "audience_id": item["id"],
                    "topic": topic,
                    "topic_type": ["content", "intent", "creative", "competitive", "utility"][idx],
                    "affinity_index": affinity,
                    "evidence_signal": ["TV plus web", "Search and site", "Social engagement", "CTV context", "Post-view action"][idx],
                    "recommendation_weight": round(clamp((affinity - 90) / 75, 0.25, 0.98), 2),
                }
            )

        for dma in item["dmas"]:
            for daypart in item["dayparts"]:
                ctv_lift = round(clamp(item["ctv"] + noise.uniform(-12, 16), 78, 168), 1)
                web_lift = round(clamp(item["web"] + noise.uniform(-10, 14), 84, 168), 1)
                social_lift = round(clamp(item["social"] + noise.uniform(-11, 13), 80, 166), 1)
                budget_weight = round(clamp((ctv_lift * 0.45 + web_lift * 0.32 + social_lift * 0.23 - 85) / 80, 0.18, 0.95), 2)
                channel = "CTV plus digital retargeting"
                if social_lift > ctv_lift and social_lift > web_lift:
                    channel = "Social proof plus web retargeting"
                elif web_lift > ctv_lift + 8:
                    channel = "Contextual web plus conversion retargeting"
                dma_rows.append(
                    {
                        "audience_id": item["id"],
                        "dma": dma,
                        "daypart": daypart,
                        "ctv_lift_index": ctv_lift,
                        "web_lift_index": web_lift,
                        "social_lift_index": social_lift,
                        "budget_weight": budget_weight,
                        "recommended_channel": channel,
                    }
                )

        tactic_templates = [
            ("Smart contextual audience", "Open web and CTV", f"Lead with {item['topics'][0]} and {item['topics'][1]} language", 7.5, "Audience manager"),
            ("Custom audience extension", "DSP", f"Extend from {item['topics'][2]} behavior into lookalike reach", 5.8, "Sales strategy"),
            ("CTV daypart test", "CTV and linear planning", f"Test {item['dayparts'][0].lower()} creative against {item['dayparts'][1].lower()} reach", 4.9, "Discovery analyst"),
            ("Measurement holdout", "Measurement", f"Separate exposed and control response for {item['kpi']}", 3.4, "Analytics"),
        ]
        for tactic, surface, creative, lift, owner in tactic_templates:
            confidence = round(clamp(row["measurement_confidence"] + noise.uniform(-9, 7), 52, 94), 1)
            activation_rows.append(
                {
                    "audience_id": item["id"],
                    "tactic": tactic,
                    "surface": surface,
                    "creative_angle": creative,
                    "expected_lift_pct": round(clamp(lift + (row["discovery_score"] - 110) / 10 + noise.uniform(-1.2, 1.5), 1.8, 12.5), 1),
                    "confidence": confidence,
                    "effort": "Low" if tactic != "Measurement holdout" else "Medium",
                    "owner": owner,
                    "next_step": "Include in client package" if confidence >= 72 else "Validate before client readout",
                }
            )

        qa_templates = [
            ("Audience definition", "Segment logic documented", "Pass", "Low", "Discovery analyst", "Keep definition in package appendix"),
            ("Identity coverage", "Household match rate above planning floor", "Pass" if match_rate_pct >= 33 else "Watch", "Medium", "Platform specialist", "Add confidence caveat if below floor"),
            ("Measurement", "Pixel or event mapping aligned to KPI", "Pass" if measurement_confidence >= 72 else "Watch", "High", "Analytics", "Confirm conversion event before activation"),
            ("Narrative", "Client-ready who what when where story", "Pass", "Low", "Sales strategy", "Review for non-technical language"),
            ("Activation", "DSP and SSP path mapped", "Pass" if activation_readiness >= 70 else "Watch", "Medium", "Activation lead", "Confirm audience export and deal path"),
        ]
        for area, check, status, severity, owner, remediation in qa_templates:
            qa_rows.append(
                {
                    "audience_id": item["id"],
                    "check_area": area,
                    "check_name": check,
                    "status": status,
                    "severity": severity,
                    "owner": owner,
                    "remediation": remediation,
                }
            )

        package_templates = [
            ("Business question", item["question"], "State the client problem before showing data."),
            ("Audience definition", item["persona"], "Translate data signals into a human audience."),
            ("Content and topic evidence", ", ".join(item["topics"][:3]), "Show why the audience is addressable now."),
            ("Where and when to reach", f"{item['dmas'][0]} and {item['dayparts'][0]}", "Connect geographic and daypart lift to media planning."),
            ("Activation recommendation", row["package_recommendation"], "Close with a clear next action and caveat."),
        ]
        for order, (section, detail, purpose) in enumerate(package_templates, start=1):
            package_rows.append(
                {
                    "audience_id": item["id"],
                    "section_order": order,
                    "section_name": section,
                    "detail": detail,
                    "analyst_purpose": purpose,
                }
            )

    return audience_rows, topic_rows, dma_rows, activation_rows, qa_rows, package_rows


def write_docs(audiences, topics, dmas, activations, qa, package_sections):
    ranked = sorted(audiences, key=lambda row: row["discovery_score"], reverse=True)
    top = ranked[0]
    watch = [row for row in ranked if row["package_recommendation"] != "Lead package"]
    avg_score = sum(row["discovery_score"] for row in audiences) / len(audiences)
    avg_confidence = sum(row["measurement_confidence"] for row in audiences) / len(audiences)
    total_households = sum(row["match_households_m"] for row in audiences)

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS / "priority_queue.csv", ranked, list(audiences[0].keys()))

    (ANALYSIS / "executive_findings.md").write_text(
        f"""# Executive Findings

## What I Analyzed

I generated a deterministic synthetic Discovery package model with {len(audiences)} audience segments, {len(topics)} topic-affinity records, {len(dmas)} DMA and daypart planning rows, {len(activations)} activation recommendations, {len(qa)} QA checks, and {len(package_sections)} client package sections.

## Findings

- The top-ranked package is **{top['audience_name']}** with a Discovery score of {top['discovery_score']}.
- The modeled package universe represents {total_households:.1f} million matched households across advertiser verticals.
- Average measurement confidence is {avg_confidence:.1f}, which means the analyst should include confidence notes instead of treating all audience stories equally.
- {len(watch)} audiences should be positioned as test packages or caveated stories instead of lead packages.

## Recommendation

Use the priority queue to decide which Discovery packages should lead the next client conversation, then use the story builder to translate the strongest package into who, what, when, where, activation, and measurement language.
""",
        encoding="utf-8",
    )

    (ANALYSIS / "analysis_plan.md").write_text(
        """# Analysis Plan

1. Frame the client business question and primary KPI.
2. Build an audience definition that a seller, agency planner, and client can all repeat.
3. Score each audience using topic affinity, action propensity, cross-screen behavior, scale, measurement confidence, and activation readiness.
4. Select the best package recommendation and caveats for the client stage.
5. Convert the output into a Discovery package: who to reach, what they care about, when and where to reach them, how to activate, and what to validate.
6. Review QA checks before presenting the package externally.
""",
        encoding="utf-8",
    )

    (ANALYSIS / "sql_checks.sql").write_text(
        """-- SQL checks mirror the synthetic CSV outputs in this public portfolio artifact.

-- 1. Audience records should have positive scale and clear KPI ownership.
select audience_id, audience_name
from audience_segments
where match_households_m <= 0
   or primary_kpi is null;

-- 2. Every audience should have package sections for a client-ready story.
select audience_id, count(*) as section_count
from package_sections
group by audience_id
having count(*) < 5;

-- 3. Measurement caveats should be visible for low-confidence package candidates.
select audience_id, audience_name, measurement_confidence, package_recommendation
from audience_segments
where measurement_confidence < 72
  and package_recommendation not like '%caveat%';

-- 4. Activation plans should map to at least three surfaces per audience.
select audience_id, count(distinct surface) as surface_count
from activation_plan
group by audience_id
having count(distinct surface) < 3;
""",
        encoding="utf-8",
    )

    (DATA / "README.md").write_text(
        f"""# Data Sources

All data in this folder is deterministic synthetic data for a public adtech audience Discovery portfolio artifact. It does not represent any real advertiser, agency, publisher, platform, campaign, household, device, or customer record.

The generator uses seed `{SEED}` and models the workflow structure of an audience insights analyst preparing client-facing Discovery packages. Public product research informed the structure of the workflow, but no proprietary platform data is used.

## Generated Files

- `audience_segments.csv`: {len(audiences)} synthetic audience segments with business questions, KPIs, indices, confidence scores, and package recommendations.
- `topic_affinity.csv`: {len(topics)} modeled topic, keyword, and content-affinity signals.
- `dma_daypart_signals.csv`: {len(dmas)} planning rows that connect DMA, daypart, lift indices, budget weights, and recommended channel paths.
- `activation_plan.csv`: {len(activations)} activation recommendations across contextual audiences, DSP paths, CTV tests, and measurement holdouts.
- `qa_checks.csv`: {len(qa)} package-readiness checks for audience definition, identity coverage, measurement, narrative, and activation.
- `package_sections.csv`: {len(package_sections)} client package sections that translate data into a presentation-ready story.

## Modeling Assumptions

- Audience indices are centered around 100, where values above 100 indicate over-indexing versus a generic baseline.
- Match scale is modeled in millions of households to reflect planning-level audience sizing, not person-level data.
- Discovery score is a transparent weighted score using topic affinity, action propensity, CTV index, web index, social index, match scale, measurement confidence, and activation readiness.
- Measurement confidence is reduced when match rate, event mapping, or activation readiness are weaker, so the artifact can show caveats before client presentation.
- DMA and daypart rows are generated from each audience's screen and content behavior so planning recommendations vary by audience rather than repeating one static dashboard.
""",
        encoding="utf-8",
    )

    (ROOT / "data_dictionary.md").write_text(
        """# Data Dictionary

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
""",
        encoding="utf-8",
    )

    (ROOT / "STATUS.md").write_text(
        """# Status

- Status: upgraded through the Portfolio Artifact Upgrade Workflow.
- Current artifact: interactive Discovery package workbench with deterministic synthetic data, priority scoring, story builder, activation plan, and QA readiness surfaces.
- Safe to link as an adtech audience insights, sales support, and Discovery package portfolio artifact after changes are pushed.
""",
        encoding="utf-8",
    )


def write_app_data(audiences, topics, dmas, activations, qa, package_sections):
    payload = {
        "audiences": audiences,
        "topics": topics,
        "dmaSignals": dmas,
        "activationPlan": activations,
        "qaChecks": qa,
        "packageSections": package_sections,
        "metadata": {
            "seed": SEED,
            "generatedBy": "scripts/score_operating_data.py",
            "scope": "Synthetic public portfolio data for an adtech audience Discovery workflow.",
        },
    }
    SRC.mkdir(parents=True, exist_ok=True)
    (SRC / "app_data.js").write_text(
        "const discoveryData = " + json.dumps(payload, indent=2) + ";\n",
        encoding="utf-8",
    )


def print_summary(audiences):
    ranked = sorted(audiences, key=lambda row: row["discovery_score"], reverse=True)
    for row in ranked[:8]:
        print(
            f"{row['audience_id']}: {row['audience_name']} score={row['discovery_score']}, "
            f"confidence={row['measurement_confidence']}, readiness={row['activation_readiness']}, "
            f"recommendation={row['package_recommendation']}"
        )


def main():
    DATA.mkdir(exist_ok=True)
    ANALYSIS.mkdir(exist_ok=True)
    audiences, topics, dmas, activations, qa, package_sections = build_rows()

    write_csv(DATA / "audience_segments.csv", audiences, list(audiences[0].keys()))
    write_csv(DATA / "topic_affinity.csv", topics, list(topics[0].keys()))
    write_csv(DATA / "dma_daypart_signals.csv", dmas, list(dmas[0].keys()))
    write_csv(DATA / "activation_plan.csv", activations, list(activations[0].keys()))
    write_csv(DATA / "qa_checks.csv", qa, list(qa[0].keys()))
    write_csv(DATA / "package_sections.csv", package_sections, list(package_sections[0].keys()))

    write_docs(audiences, topics, dmas, activations, qa, package_sections)
    write_app_data(audiences, topics, dmas, activations, qa, package_sections)
    print_summary(audiences)


if __name__ == "__main__":
    main()
