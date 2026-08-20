"""
Operator model - Day 3, SQLAlchemy 2.0 ORM version.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .facility import Facility
    from .mission import Mission


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"))

    facility: Mapped["Facility"] = relationship(back_populates="operators")
    missions: Mapped[list["Mission"]] = relationship(back_populates="operator")

    def __repr__(self) -> str:
        return (f"Operator(id={self.id}, name={self.name!r}, "
                f"facility_id={self.facility_id})")



"""
Operator model - Day 1 Answer Key (Phase B / Business Question #2).

Not part of the original ERD's explicit entity list, but implied by
Mission.operator_id. Follows the exact same registry/find_by_id pattern
established by Facility and Robot.


from typing import ClassVar


class Operator:
    registry: ClassVar[list["Operator"]] = []

    def __init__(self, operator_id: int, name: str, facility_id: int):
        self.id = operator_id
        self.name = name
        self.facility_id = facility_id
        Operator.registry.append(self)

    @classmethod
    def find_by_id(cls, operator_id: int) -> "Operator | None":
        for operator in cls.registry:
            if operator.id == operator_id:
                return operator
        return None

    def __repr__(self) -> str:
        return (f"Operator(id={self.id}, name={self.name!r}, "
                f"facility_id={self.facility_id})")
"""