"""
RoboPulse Fleet Command Center
Day 4 Answer Key - Pydantic v2 schema for the discrepancy report.
Day 5 Answer Key - additions for challenge
"""

from pydantic import BaseModel, ConfigDict

from app.models import MissionPriority, MissionStatus


class DiscrepancyRead(BaseModel):
    mission_id: int
    title: str
    robot_facility_id: int
    operator_facility_id: int

    model_config = ConfigDict(from_attributes=True)


class MissionStatusUpdate(BaseModel):
    status:MissionStatus


class MissionRead(BaseModel):
    id: int
    title: str
    priority: MissionPriority
    status: MissionStatus
    robot_id: int
    operator_id: int

    model_config = ConfigDict(from_attributes=True)