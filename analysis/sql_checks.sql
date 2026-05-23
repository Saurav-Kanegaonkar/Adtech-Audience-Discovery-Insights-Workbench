-- SQL checks mirror the synthetic CSV outputs in this public portfolio artifact.

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
