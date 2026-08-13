"""
RoboPulse Fleet Command Center
Day 4 Answer Key - Mission endpoints.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import Mission, MissionPriority, Operator, Robot
from app.schemas.mission import DiscrepancyRead

router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("/discrepancies", response_model=list[DiscrepancyRead])
async def list_colocation_discrepancies(
    priority: MissionPriority | None = Query(
        default=None,
        description="Only return discrepancies for missions of this priority.",
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Business Question #2: Co-Location Discrepancy - a fourth time.
    Day 1: Python. Day 2: raw SQL. Day 3: async ORM script. Today:
    the same three-table JOIN, reachable at
    GET /missions/discrepancies, with an optional priority filter.

    Selects only the four columns the response actually needs,
    rather than full Mission/Robot/Operator objects - see the
    Research Prompts in day04_demo_and_challenge.md for the tradeoff
    this makes against day3_challenge.py's find_colocation_discrepancies_orm.
    """
    statement = (
        select(
            Mission.id.label("mission_id"),
            Mission.title,
            Robot.facility_id.label("robot_facility_id"),
            Operator.facility_id.label("operator_facility_id"),
        )
        .join(Robot, Robot.id == Mission.robot_id)
        .join(Operator, Operator.id == Mission.operator_id)
        .where(Robot.facility_id != Operator.facility_id)
    )

    if priority is not None:
        statement = statement.where(Mission.priority == priority)

    statement = statement.order_by(Mission.id)

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]