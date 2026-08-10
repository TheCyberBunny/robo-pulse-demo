"""
Package init - lets us write:
    from app.models import Robot, Facility
instead of:
    from app.models.robot import Robot
    from app.models.facility import Facility
"""

from .enums import RobotStatus, MissionPriority, MissionStatus
from .facility import Facility
from .robot import Robot
from .mission import Mission
from .diagnostic_log import DiagnosticLog
from .operator import Operator


#this declares the list of public objects of that module, as interpreted by import *
#similar to java's public/private access modifiers, this is a way to control what is exposed to other modules
__all__ = [
    "RobotStatus", "MissionPriority", "MissionStatus",
    "Facility", "Robot", "Mission", "DiagnosticLog", "Operator",
]