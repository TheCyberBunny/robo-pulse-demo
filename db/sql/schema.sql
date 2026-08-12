-- ============================================================
-- RoboPulse Fleet Command Center - Day 2 Schema
--
-- Why this file exists: Day 1 modeled Facility/Robot/Mission/
-- DiagnosticLog as plain Python classes living only in memory - the
-- moment the script ended, the data was gone. Today we give that
-- exact same shape a permanent home in PostgreSQL. Day 3's SQLAlchemy
-- ORM will eventually GENERATE SQL like this FOR us automatically -
-- we're writing it by hand once, today, specifically so the ORM never
-- feels like an unexplainable black box later this week.
-- ============================================================

-- ------------------------------------------------------------
-- STEP 1: Enumerated types
--
-- Why this step comes first: Day 1 used Python's `enum.Enum` to
-- restrict RobotStatus / MissionPriority / MissionStatus to a fixed
-- set of valid values. PostgreSQL has its own native ENUM type that
-- enforces the exact same rule - but at the DATABASE level. Even a
-- bug in a completely different application, years from now, cannot
-- write an invalid status into this table; the database itself
-- rejects it. These are defined before any table because the tables
-- below reference them by name.
-- ------------------------------------------------------------
CREATE TYPE robot_status AS ENUM ('Idle', 'In-Mission', 'Maintenance', 'Offline');
CREATE TYPE mission_priority AS ENUM ('Low', 'Medium', 'Critical');
CREATE TYPE mission_status AS ENUM ('Pending', 'In-Progress', 'Completed', 'Failed');

-- ------------------------------------------------------------
-- STEP 2: facilities table
--
-- Why this step comes next: both robots and operators will reference
-- a facility via a foreign key. PostgreSQL physically refuses to
-- create a foreign key that points at a table that doesn't exist yet
-- - so the table being referenced always has to be created FIRST.
-- facilities has no foreign keys of its own, making it the natural
-- starting point.
-- ------------------------------------------------------------
CREATE TABLE facilities (
    id              SERIAL PRIMARY KEY,        -- auto-incrementing integer; Postgres assigns this, we never set it by hand
    name            VARCHAR(100) NOT NULL,
    location_region VARCHAR(50)  NOT NULL,
    capacity        INTEGER      NOT NULL,
    supervisor_id   INTEGER      NOT NULL       -- intentionally NOT a foreign key: supervisors/employees aren't modeled as their own table in this schema
);

-- ------------------------------------------------------------
-- STEP 3: operators table
--
-- Why this step comes next: Operator was introduced informally in
-- Python on Day 1's student challenge (Business Question #2). Today
-- it becomes a real table, so `missions.operator_id` (STEP 5) will
-- have something concrete to point at. Depends on facilities (STEP 2)
-- existing first, because of the foreign key below.
-- ------------------------------------------------------------
CREATE TABLE operators (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    facility_id INTEGER NOT NULL REFERENCES facilities(id)   -- FOREIGN KEY: every operator belongs to exactly one facility
);

-- ------------------------------------------------------------
-- STEP 4: robots table
--
-- Why this step comes next: mirrors Day 1's Robot Python class
-- field-for-field, so the mapping between "the class we wrote
-- yesterday" and "the table we're writing today" stays obvious.
-- Depends on facilities (STEP 2) existing first.
-- ------------------------------------------------------------
CREATE TABLE robots (
    id            SERIAL PRIMARY KEY,
    serial_number VARCHAR(50)  NOT NULL UNIQUE,              -- UNIQUE: the database now enforces "no two robots share a serial," a rule Day 1's Python never actually enforced
    model         VARCHAR(100) NOT NULL,
    status        robot_status NOT NULL DEFAULT 'Idle',      -- reuses the ENUM type from STEP 1
    battery_level NUMERIC(5,2) NOT NULL CHECK (battery_level BETWEEN 0 AND 100),  -- CHECK constraint: the database-level version of Day 1's Robot._validate_battery()
    facility_id   INTEGER NOT NULL REFERENCES facilities(id)
);

-- ------------------------------------------------------------
-- STEP 5: missions table
--
-- Why this step comes next: the first table with TWO foreign keys, so
-- it can't be created until BOTH robots (STEP 4) and operators
-- (STEP 3) already exist. This is also the table Business Question #2
-- (co-location discrepancy) and Business Question #3 (reliability
-- metrics) will query against later today.
-- ------------------------------------------------------------
CREATE TABLE missions (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(150)     NOT NULL,
    priority    mission_priority NOT NULL,
    status      mission_status   NOT NULL DEFAULT 'Pending',
    robot_id    INTEGER NOT NULL REFERENCES robots(id),
    operator_id INTEGER NOT NULL REFERENCES operators(id)
);

-- ------------------------------------------------------------
-- STEP 6: diagnostic_logs table
--
-- Why this step comes last: the last link in the dependency chain -
-- it can't exist until missions (STEP 5) does, since every log
-- attaches to exactly one mission.
-- ------------------------------------------------------------
CREATE TABLE diagnostic_logs (
    id         SERIAL PRIMARY KEY,
    mission_id INTEGER NOT NULL REFERENCES missions(id),
    file_url   TEXT NOT NULL,                    -- TEXT has no length cap, unlike VARCHAR(n) - S3 URLs can get long
    notes      TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()  -- the DATABASE sets this automatically now - no more of Day 1's "shared default timestamp" gotcha, since NOW() is re-evaluated on every single INSERT
);