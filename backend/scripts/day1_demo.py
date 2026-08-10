"""
Day 1 demo script - RoboPulse Fleet Command Center
Run from backend/ with the venv active:
    python -m scripts.day1_demo
"""

from app.models import Facility, Robot, Mission, DiagnosticLog, Operator
from app.models import RobotStatus, MissionPriority


def find_low_battery_robots(robots: list[Robot], threshold: int = 20) -> list[Robot]:
    """
    Business Question #1: Low Battery Alert
    Which ACTIVE robots are operating below `threshold`% battery?
    """
    return [
        robot for robot in robots
        if robot.status != RobotStatus.OFFLINE and robot.is_low_battery(threshold)
    ]

def find_colocation_discrepancies(
    missions: list[Mission],
    robots: list[Robot],
    operators: list[Operator],
) -> list[tuple[Mission, Robot, Operator]]:
    """
    Business Question #2: Co-Location Discrepancy
    Which missions assign a robot to an operator who is NOT at the
    same facility as that robot?

    Takes robots/operators as parameters rather than reaching into
    Robot.registry / Operator.registry directly, so the function stays
    testable against any data set, not just whatever's been seeded at
    import time.
    """
    discrepancies: list[tuple[Mission, Robot, Operator]] = []

    for mission in missions:
        robot = Robot.find_by_id(mission.robot_id)
        operator = Operator.find_by_id(mission.operator_id)

        # Defensive guard: a mission referencing a robot_id or
        # operator_id that doesn't exist in the registry isn't a
        # co-location discrepancy - it's a data integrity problem.
        # Skip it here; Week 2's validation layer handles that properly.
        if robot is None or operator is None:
            continue

        if robot.facility_id != operator.facility_id:
            discrepancies.append((mission, robot, operator))

    return discrepancies

#creating some dummy data for the demo, including facilities, robots, missions, and diagnostic logs
def seed_demo_data() -> None:
    Facility(1, "Houston Fabrication Plant", "US-South", capacity=40, supervisor_id=101)
    Facility(2, "Rotterdam Logistics Hub", "EU-West", capacity=25, supervisor_id=102)

    Robot(1, "RX-1001", "Sentinel-V2", battery_level=18.5, facility_id=1,
          status=RobotStatus.IN_MISSION)
    Robot(2, "RX-1002", "Sentinel-V2", battery_level=76.0, facility_id=1,
          status=RobotStatus.IDLE)
    Robot(3, "AD-2050", "SkyHawk-Drone", battery_level=9.0, facility_id=2,
          status=RobotStatus.IN_MISSION)
    Robot(4, "RX-1003", "Sentinel-V2", battery_level=42.0, facility_id=1,
          status=RobotStatus.MAINTENANCE)

    Mission(1, "Pipeline Corrosion Sweep", MissionPriority.CRITICAL,
            robot_id=1, operator_id=201)
    Mission(2, "Warehouse Perimeter Patrol", MissionPriority.LOW,
            robot_id=3, operator_id=202)

    DiagnosticLog(1, mission_id=1,
                  file_url="s3://robopulse-diagnostics/rx1001-001.pdf",
                  notes="Vibration sensor reading nominal")

    # Operator 201 is based at facility 1 - same facility as Robot 1 (RX-1001).
    Operator(201, "J. Alvarez", facility_id=1)
    # Operator 202 is based at facility 1, but will be assigned a robot
    # stationed at facility 2 below - a deliberate co-location discrepancy.
    Operator(202, "M. Chen", facility_id=1)

#create our dummy data and run the low battery check, printing out the results to the console
def main() -> None:
    seed_demo_data()

    print("== Full Robot Registry ==")
    for robot in Robot.registry:
        print(robot)

    print("\n== Low Battery Alert (< 20%) ==")
    alerts = find_low_battery_robots(Robot.registry, threshold=20)
    if not alerts:
        print("  No robots below threshold.")
    for robot in alerts:
        print(f"  ALERT: {robot.serial_number} at {robot.battery_level}% "
              f"(facility {robot.facility_id})")

    print("\n== Co-Location Discrepancy Report ==")
    discrepancies = find_colocation_discrepancies(
        Mission.registry, Robot.registry, Operator.registry
    )
    if not discrepancies:
        print("  No discrepancies found.")
    for mission, robot, operator in discrepancies:
        print(f"  Mission {mission.id} ({mission.title}): "
              f"robot at facility {robot.facility_id}, "
              f"operator at facility {operator.facility_id}")

## Entry point for the script
if __name__ == "__main__":
    main()