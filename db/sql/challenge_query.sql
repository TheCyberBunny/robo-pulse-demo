-- ============================================================
-- RoboPulse Fleet Command Center - Day 2 Answer Key
-- Business Question #2: Co-Location Discrepancy (SQL version)
--
-- Why this file exists: Day 1's Phase B answered this same question
-- in plain Python, looping through in-memory lists by hand with
-- Robot.find_by_id() / Operator.find_by_id(). Today's version asks
-- PostgreSQL to do that same lookup work natively, as a JOIN.
-- ============================================================

-- ------------------------------------------------------------
-- STEP 1: start from missions
-- Why this table first: a "discrepancy" is a property OF a mission -
-- specifically, a mismatch between the facility of the robot it
-- assigns and the facility of the operator it assigns. Every other
-- table in this query exists only to answer "which facility does
-- THIS mission's robot/operator belong to?"
-- ------------------------------------------------------------

-- ------------------------------------------------------------
-- STEP 2: JOIN robots - answers "where is the assigned ROBOT stationed?"
-- Why this join: missions.robot_id is just a bare integer on its own.
-- Joining robots pulls in that robot's actual facility_id so it can be
-- compared against the operator's facility_id below.
-- ------------------------------------------------------------

-- ------------------------------------------------------------
-- STEP 3: JOIN operators - answers "where is the assigned OPERATOR based?"
-- Why this join: same reasoning as Step 2, but for the operator side.
-- This is the JOIN that Day 1's Python didn't have a table for at
-- all - Operator only existed as a plain Python class then.
-- ------------------------------------------------------------

-- ------------------------------------------------------------
-- STEP 4: WHERE the two facility_id values disagree
-- Why this comes last: Steps 2 and 3 make BOTH facility_id values
-- available on the same result row. This WHERE clause is the actual
-- business rule - everything above it is just plumbing to get both
-- values into the same place for comparison.
-- ------------------------------------------------------------
SELECT
    m.id    AS mission_id,
    m.title,
    r.facility_id AS robot_facility_id,
    o.facility_id AS operator_facility_id
FROM missions m
JOIN robots r     ON r.id = m.robot_id
JOIN operators o  ON o.id = m.operator_id
WHERE r.facility_id != o.facility_id;