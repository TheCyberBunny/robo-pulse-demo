"""
Robot model - Day 1 plain-Python version.
"""

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