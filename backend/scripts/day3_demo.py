"""
Day 3 demo script - RoboPulse Fleet Command Center
Queries the SAME robopulse_dev data Day 2's seed.sql already loaded.
Nothing gets re-seeded today - this proves the ORM models line up
with data that already exists.

Run from backend/ with the venv active:
    python -m scripts.day3_demo
"""

import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import AsyncSessionLocal
from app.models import Robot, RobotStatus


async def find_low_battery_robots(session, threshold: int = 20) -> list[Robot]:
    """
    Business Question #1: Low Battery Alert - third time answering it.
    Day 1: a Python list comprehension over an in-memory list.
    Day 2: a SQL WHERE clause, typed by hand into demo_queries.sql.
    Today: the same WHERE clause, generated FOR us from a Python
    expression - Robot.battery_level < threshold compiles down to
    the same SQL Day 2 wrote by hand.
    """

    #statement object is a SQLAlchemy construct that represents a SQL SELECT statement.
    statement = (
        select(Robot)
       .options(selectinload(Robot.facility))
        .where(Robot.status != RobotStatus.OFFLINE, Robot.battery_level < threshold)
        .order_by(Robot.id)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def main() -> None:
    async with AsyncSessionLocal() as session:
        print("== Full Robot Registry (via ORM) ==")
        all_robots_stmt = select(Robot).options(selectinload(Robot.facility)).order_by(Robot.id)
        all_robots = await session.execute(all_robots_stmt)
        for robot in all_robots.scalars():
            print(f"{robot!r} -> facility: {robot.facility.name}")

        print("\n== Low Battery Alert (< 20%) ==")
        alerts = await find_low_battery_robots(session, threshold=20)
        if not alerts:
            print("  No robots below threshold.")
        for robot in alerts:
            print(f"  ALERT: {robot.serial_number} at {robot.battery_level}% "
                  f"(facility: {robot.facility.name})")

if __name__ == "__main__":
    asyncio.run(main())