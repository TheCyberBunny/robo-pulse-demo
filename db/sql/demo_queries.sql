-- ============================================================
-- RoboPulse Fleet Command Center - Day 2 Demo Queries
--
-- Why this file exists: schema.sql defined WHERE data lives, seed.sql
-- put data there. This file is where we actually DO something with
-- it - the full CRUD cycle, then two JOIN queries that answer real
-- business questions from the problem statement. Run block by block
-- during the live demo rather than all at once, so each result can be
-- discussed before moving to the next.
-- ============================================================

-- ------------------------------------------------------------
-- STEP 1: CRUD - Read (SELECT)
--
-- Why this step comes first: before touching any data, confirm the
-- seed actually loaded correctly. This is the "R" in CRUD, and the
-- safest possible place to start - reading data can't damage anything,
-- unlike the Create/Update/Delete steps that follow.
-- ------------------------------------------------------------
SELECT * FROM robots ORDER BY id;

-- ------------------------------------------------------------
-- STEP 2: CRUD - Create (INSERT)
--
-- Why this step comes next: seed.sql already showed bulk INSERT with
-- hardcoded ids; this demonstrates the single-row INSERT shape a real
-- application actually uses - no id specified (SERIAL generates it),
-- and RETURNING hands back the generated id immediately, the way an
-- API would need it to build a response.
-- ------------------------------------------------------------
INSERT INTO robots (serial_number, model, status, battery_level, facility_id)
VALUES ('RX-1004', 'Sentinel-V2', 'Idle', 88.0, 1)
RETURNING id, serial_number;

-- ------------------------------------------------------------
-- STEP 3: CRUD - Update (UPDATE)
--
-- Why this step comes next: robots change state constantly in the
-- real system - a battery drains, a mission starts. UPDATE is how
-- that state change gets saved. Always pair UPDATE with a WHERE
-- clause: run this same statement WITHOUT the WHERE line and every
-- single robot in the table gets set to 'In-Mission' at 85% battery -
-- worth demonstrating as a cautionary example on a throwaway table if
-- time allows.
-- ------------------------------------------------------------
UPDATE robots
SET status = 'In-Mission', battery_level = 85.0
WHERE serial_number = 'RX-1004';

-- ------------------------------------------------------------
-- STEP 4: CRUD - Delete (DELETE)
--
-- Why this step comes next: completes the CRUD cycle by removing the
-- row STEP 2 created. Doing this keeps the seed data exactly
-- reproducible for every future class run - anyone re-running
-- schema.sql + seed.sql + demo_queries.sql from scratch gets identical
-- results. Same warning as UPDATE: DELETE with no WHERE clause empties
-- the ENTIRE table, not just one row.
-- ------------------------------------------------------------
DELETE FROM robots WHERE serial_number = 'RX-1004';

-- ------------------------------------------------------------
-- STEP 5: Business Question #1, revisited - Low Battery Alert
--
-- Why this step comes next: Day 1 answered this exact question with a
-- Python list comprehension looping over an in-memory list by hand.
-- Same question, same two robots come back, but now PostgreSQL's
-- query planner is doing the filtering - work that can be indexed and
-- optimized later, which a Python for-loop never could be.
-- ------------------------------------------------------------
SELECT serial_number, battery_level, facility_id
FROM robots
WHERE status != 'Offline' AND battery_level < 20
ORDER BY id;

-- ------------------------------------------------------------
-- STEP 6: JOIN - connecting missions to the robots that ran them
--
-- Why this step comes next: missions.robot_id is just a bare integer -
-- on its own, meaningless to a human reading query results. JOIN
-- pulls in the actual matching robot row in the SAME query, instead
-- of looking it up separately - exactly what Robot.find_by_id() did
-- by hand, one call at a time, in yesterday's Python.
-- ------------------------------------------------------------
SELECT m.id, m.title, m.status, r.serial_number, r.model
FROM missions m
JOIN robots r ON r.id = m.robot_id
ORDER BY m.id;

-- ------------------------------------------------------------
-- STEP 7: Business Question #3 - Reliability Metrics (JOIN + aggregate)
--
-- Why this step comes last: this is the query a real analytics
-- endpoint would actually run. It combines STEP 6's JOIN pattern with
-- GROUP BY aggregation - two ideas taught separately, now combined
-- into one query that genuinely answers a business question from the
-- problem statement: "What is the mission success/failure ratio
-- broken down by robot model?"
-- ------------------------------------------------------------
SELECT
    r.model,
    COUNT(m.id)                                              AS total_missions,
    SUM(CASE WHEN m.status = 'Completed' THEN 1 ELSE 0 END)  AS completed_count,
    SUM(CASE WHEN m.status = 'Failed'    THEN 1 ELSE 0 END)  AS failed_count
FROM robots r
JOIN missions m ON m.robot_id = r.id
GROUP BY r.model
ORDER BY r.model;