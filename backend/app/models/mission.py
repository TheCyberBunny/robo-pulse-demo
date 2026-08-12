"""
Mission model - Day 3, SQLAlchemy 2.0 ORM version.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import MissionPriority, MissionStatus

if TYPE_CHECKING:
    from .diagnostic_log import DiagnosticLog
    from .operator import Operator
    from .robot import Robot


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    priority: Mapped[MissionPriority] = mapped_column(
        SqlEnum(
            MissionPriority,
            name="mission_priority",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        )
    )
    status: Mapped[MissionStatus] = mapped_column(
        SqlEnum(
            MissionStatus,
            name="mission_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=MissionStatus.PENDING,
    )
    robot_id: Mapped[int] = mapped_column(Integer, ForeignKey("robots.id"))
    operator_id: Mapped[int] = mapped_column(Integer, ForeignKey("operators.id"))

    robot: Mapped["Robot"] = relationship(back_populates="missions")
    operator: Mapped["Operator"] = relationship(back_populates="missions")
    diagnostic_logs: Mapped[list["DiagnosticLog"]] = relationship(back_populates="mission")

    def mark_completed(self) -> None:
        self.status = MissionStatus.COMPLETED

    def mark_failed(self) -> None:
        self.status = MissionStatus.FAILED

    def __repr__(self) -> str:
        return (f"Mission(id={self.id}, title={self.title!r}, "
                f"priority={self.priority.value}, status={self.status.value})")




"""
Mission model - Day 1 plain-Python version.


from typing import ClassVar

from .enums import MissionPriority, MissionStatus


class Mission:
    registry: ClassVar[list["Mission"]] = []

    def __init__(self, mission_id: int, title: str, priority: MissionPriority,
                 robot_id: int, operator_id: int,
                 status: MissionStatus = MissionStatus.PENDING):
        self.id = mission_id
        self.title = title
        self.priority = priority
        self.status = status
        self.robot_id = robot_id
        self.operator_id = operator_id
        Mission.registry.append(self)

    #note that we are using the MissionStatus enum to set the status of the mission,
    #which is a good practice to ensure that the status is always one of the predefined values
    def mark_completed(self) -> None:
        self.status = MissionStatus.COMPLETED

    def mark_failed(self) -> None:
        self.status = MissionStatus.FAILED

    @classmethod
    def find_by_id(cls, mission_id: int) -> "Mission | None":
        for mission in cls.registry:
            if mission.id == mission_id:
                return mission
        return None

    def __repr__(self) -> str:
        return (f"Mission(id={self.id}, title={self.title!r}, "
                f"priority={self.priority.value}, status={self.status.value})")
"""