"""
Day 3 Answer Key - RoboPulse Fleet Command Center
Business Question #2 (Co-Location Discrepancy), answered a third time:
Day 1 - manual Robot.find_by_id() / Operator.find_by_id() lookups in
        plain Python.
Day 2 - a hand-written three-table SQL JOIN in challenge_query.sql.
Today - the same three-table JOIN, expressed as a SQLAlchemy 2.0
        select() with explicit .join() calls, run through the async
        engine, against the SAME already-seeded robopulse_dev data.

Run from backend/ with the venv active:
    python -m scripts.day3_challenge
"""

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import Mission, Operator, Robot


async def find_colocation_discrepancies_orm(session: AsyncSession) -> list[Mission]:
    """
    Business Question #2: Co-Location Discrepancy (ORM version).
    Which missions assign a robot to an operator who is NOT at the
    same facility as that robot?

    Mirrors day02_answer_key.md's challenge_query.sql almost exactly:
    JOIN missions -> robots -> operators, then filter on the two
    facility_id columns disagreeing. The difference today is that the
    JOIN and WHERE clause are built from Python expressions instead of
    typed as raw SQL - but PostgreSQL still does the actual filtering
    work, same as Day 2 (this function does NOT fetch everything and
    filter with a Python if-statement).

    Accepts session as a parameter, same reasoning as Day 1's
    find_colocation_discrepancies(): keeps this function testable
    against any session, not tied to a single global connection.
    """
    statement = (
        select(Mission)
        .join(Robot, Robot.id == Mission.robot_id)
        .join(Operator, Operator.id == Mission.operator_id)
        .where(Robot.facility_id != Operator.facility_id)
        .order_by(Mission.id)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def main() -> None:
    async with AsyncSessionLocal() as session:
        print("== Co-Location Discrepancy Report (via ORM) ==")
        discrepancies = await find_colocation_discrepancies_orm(session)

        if not discrepancies:
            print("  No discrepancies found.")

        for mission in discrepancies:
            # mission.robot / mission.operator are lazy-loaded here.
            # This works (unlike Step 9's crash) because we're still
            # inside the `async with AsyncSessionLocal()` block, and
            # each access below is awaited implicitly by asyncpg's
            # greenlet bridge the moment Python evaluates the
            # attribute - the trap from Step 9 was specifically about
            # touching a lazy attribute AFTER the session had already
            # done its work inside a plain, non-awaited print() call
            # chain. Being explicit with selectinload (as day3_demo.py
            # does) is still the safer habit for anything beyond a
            # quick script like this one.
            robot = await session.get(Robot, mission.robot_id)
            operator = await session.get(Operator, mission.operator_id)
            print(f"  Mission {mission.id} ({mission.title}): "
                  f"robot at facility {robot.facility_id}, "
                  f"operator at facility {operator.facility_id}")


if __name__ == "__main__":
    asyncio.run(main())