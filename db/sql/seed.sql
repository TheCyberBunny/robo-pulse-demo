-- ============================================================
-- RoboPulse Fleet Command Center - Day 2 Seed Data
--
-- Why this file exists: reuses the EXACT same values as Day 1's
-- seed_demo_data() Python function, so today's SQL query results can
-- be compared directly against yesterday's Python console output -
-- same robots, same battery levels, same facilities - just stored
-- somewhere durable now instead of in a list that vanishes on exit.
-- Run this immediately after schema.sql (\i schema.sql then
-- \i seed.sql in psql).
-- ============================================================

-- ------------------------------------------------------------
-- STEP 1: facilities first
-- Why this step comes first: every other table's foreign key
-- eventually traces back to a facility_id - these rows have to exist
-- before anything else can reference them.
-- ------------------------------------------------------------
INSERT INTO facilities (id, name, location_region, capacity, supervisor_id) VALUES
    (1, 'Houston Fabrication Plant', 'US-South', 40, 101),
    (2, 'Rotterdam Logistics Hub',   'EU-West',  25, 102);

-- ------------------------------------------------------------
-- STEP 2: operators next
-- Why this step comes next: the same two operators from Day 1's
-- Phase B answer key (J. Alvarez at facility 1, M. Chen also
-- assigned to facility 1 on paper - but about to run a mission with a
-- robot stationed at facility 2, which is what created yesterday's
-- co-location discrepancy in Python, and will again today in SQL).
-- ------------------------------------------------------------
INSERT INTO operators (id, name, facility_id) VALUES
    (201, 'J. Alvarez', 1),
    (202, 'M. Chen',    1);

-- ------------------------------------------------------------
-- STEP 3: robots
-- Why this step comes next: identical serial numbers, models, and
-- battery levels to Day 1's demo output, specifically so the Low
-- Battery Alert query later in demo_queries.sql produces the exact
-- same two robots (RX-1001 and AD-2050) that Day 1's Python found.
-- ------------------------------------------------------------
INSERT INTO robots (id, serial_number, model, status, battery_level, facility_id) VALUES
    (1, 'RX-1001', 'Sentinel-V2',   'In-Mission',  18.5, 1),
    (2, 'RX-1002', 'Sentinel-V2',   'Idle',        76.0, 1),
    (3, 'AD-2050', 'SkyHawk-Drone', 'In-Mission',   9.0, 2),
    (4, 'RX-1003', 'Sentinel-V2',   'Maintenance', 42.0, 1);

-- ------------------------------------------------------------
-- STEP 4: missions
-- Why this step comes next: missions 1 and 2 are identical to Day 1.
-- Missions 3 and 4 are NEW - added specifically so today's Reliability
-- Metrics demo (Business Question #3) has a Completed and a Failed
-- mission to aggregate over. Day 1 never had a mission leave the
-- Pending state, so there was nothing to compute a ratio from yet.
-- ------------------------------------------------------------
INSERT INTO missions (id, title, priority, status, robot_id, operator_id) VALUES
    (1, 'Pipeline Corrosion Sweep',   'Critical', 'Pending',   1, 201),
    (2, 'Warehouse Perimeter Patrol', 'Low',      'Pending',   3, 202),
    (3, 'Cooling Tower Inspection',   'Medium',   'Completed', 2, 201),
    (4, 'Fence Line Survey',          'Low',      'Failed',    4, 201);

-- ------------------------------------------------------------
-- STEP 5: diagnostic_logs
-- Why this step comes last: depends on mission 1 already existing
-- (STEP 4). Same single log entry from Day 1's demo.
-- ------------------------------------------------------------
INSERT INTO diagnostic_logs (mission_id, file_url, notes) VALUES
    (1, 's3://robopulse-diagnostics/rx1001-001.pdf', 'Vibration sensor reading nominal');

-- ------------------------------------------------------------
-- IMPORTANT: keep SERIAL sequences in sync with the hardcoded IDs
-- Why this step matters: we inserted explicit `id` values above
-- (1, 2, 3...) instead of letting SERIAL generate them. Postgres's
-- internal auto-increment counter doesn't know that happened, so the
-- VERY NEXT plain INSERT (with no id specified) would try to reuse
-- id 1 and fail with a duplicate-key error. This resets each
-- sequence to continue after the highest ID we just inserted by hand.
-- ------------------------------------------------------------
SELECT setval('facilities_id_seq', (SELECT MAX(id) FROM facilities));
SELECT setval('operators_id_seq', (SELECT MAX(id) FROM operators));
SELECT setval('robots_id_seq', (SELECT MAX(id) FROM robots));
SELECT setval('missions_id_seq', (SELECT MAX(id) FROM missions));