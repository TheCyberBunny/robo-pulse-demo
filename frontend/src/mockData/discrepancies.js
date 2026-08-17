/**
 * RoboPulse Fleet Command Center
 * Day 6 Answer Key - mock discrepancy data, shaped to match
 * GET /missions/discrepancies' verified response from
 * day04_answer_key.md, using JS camelCase instead of the API's
 * snake_case JSON keys. Day 7 replaces this file with a real Axios
 * call; DiscrepancyCard/DiscrepancyList below won't need to change
 * either way.
 */
export const mockDiscrepancies = [
  {
    missionId: 2,
    title: 'Warehouse Perimeter Patrol',
    robotFacilityId: 2,
    operatorFacilityId: 1,
  },
];