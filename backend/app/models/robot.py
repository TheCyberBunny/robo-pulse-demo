"""
Robot model - Day 3, SQLAlchemy 2.0 ORM version.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import RobotStatus

if TYPE_CHECKING:
    from .facility import Facility
    from .mission import Mission


class Robot(Base):
    __tablename__ = "robots"

    #here we define a table-level constraint to ensure that the battery_level column
    # is always between 0 and 100. This is a good practice to enforce data integrity
    __table_args__ = (
        CheckConstraint("battery_level BETWEEN 0 AND 100", name="battery_level_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(String(50), unique=True)
    model: Mapped[str] = mapped_column(String(100))
    status: Mapped[RobotStatus] = mapped_column(
        SqlEnum(
            RobotStatus,
            name="robot_status",
            # Defines how the enum values are stored in the database. 
            # In this case, we store the string representation of the enum members.
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=RobotStatus.IDLE,
    )
    battery_level: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"))

    facility: Mapped["Facility"] = relationship(back_populates="robots")
    missions: Mapped[list["Mission"]] = relationship(back_populates="robot")

    LOW_BATTERY_THRESHOLD: int = 20

    def is_low_battery(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold is not None else Robot.LOW_BATTERY_THRESHOLD
        return self.battery_level < limit

    def needs_maintenance(self) -> bool:
        return self.status == RobotStatus.MAINTENANCE

    def __repr__(self) -> str:
        return (f"Robot(serial={self.serial_number!r}, model={self.model!r}, "
                f"battery={self.battery_level}%, status={self.status.value})")
    



"""
Robot model - Day 1 plain-Python version.


from typing import ClassVar

from .enums import RobotStatus


class Robot:

    #this is a class attribute that will hold all instances of Robot
    registry: ClassVar[list["Robot"]] = []
    #a class attribute used to determine if a robot's battery level is considered low
    LOW_BATTERY_THRESHOLD: ClassVar[int] = 20

    #the constructor method for the Robot class
    def __init__(self, robot_id: int, serial_number: str, model: str,
                 battery_level: float, facility_id: int,
                 status: RobotStatus = RobotStatus.IDLE):
        self.id = robot_id
        self.serial_number = serial_number
        self.model = model
        self.status = status
        self.facility_id = facility_id
        self.battery_level = self._validate_battery(battery_level)
        Robot.registry.append(self)

    #a static method that validates the battery level of a robot
    #the annotation @staticmethod indicates that this method is a static method, 
    #which means it can be called on the class itself, rather than on an instance of the class
    @staticmethod
    def _validate_battery(level: float) -> float:
        if level < 0:
            print(f"Warning: battery_level {level} below 0, clamping to 0")
            return 0.0
        if level > 100:
            print(f"Warning: battery_level {level} above 100, clamping to 100")
            return 100.0
        return float(level)

    #a method that checks if the robot's battery level is below a certain threshold
    #if no threshold is provided, it uses the class attribute LOW_BATTERY_THRESHOLD
    def is_low_battery(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold is not None else Robot.LOW_BATTERY_THRESHOLD
        return self.battery_level < limit

    #a method that checks if the robot's status is set to maintenance
    def needs_maintenance(self) -> bool:
        return self.status == RobotStatus.MAINTENANCE

    #a class method that finds a Robot instance by its ID
    @classmethod
    def find_by_id(cls, robot_id: int) -> "Robot | None":
        for robot in cls.registry:
            if robot.id == robot_id:
                return robot
        return None

    #a class method that finds a Robot instance by its serial number
    def __repr__(self) -> str:
        return (f"Robot(serial={self.serial_number!r}, model={self.model!r}, "
                f"battery={self.battery_level}%, status={self.status.value})")
"""