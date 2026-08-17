/**
 * RoboPulse Fleet Command Center
 * Day 6 - mock robot data, mirroring Day 2's seed.sql exactly, so
 * today's UI shows the same fleet every prior day's tool has already
 * queried. Day 7 replaces this file with a real Axios call to
 * GET /robots - RobotCard/RobotList below won't need to change at
 * all when that happens, since both only ever consume a `robots`
 * array passed in as a prop, regardless of where it came from.
 */
export const mockRobots = [
  { id: 1, serialNumber: 'RX-1001', model: 'Sentinel-V2', batteryLevel: 18.5, status: 'In-Mission', facilityId: 1 },
  { id: 2, serialNumber: 'RX-1002', model: 'Sentinel-V2', batteryLevel: 76.0, status: 'Idle', facilityId: 1 },
  { id: 3, serialNumber: 'AD-2050', model: 'SkyHawk-Drone', batteryLevel: 9.0, status: 'In-Mission', facilityId: 2 },
  { id: 4, serialNumber: 'RX-1003', model: 'Sentinel-V2', batteryLevel: 42.0, status: 'Maintenance', facilityId: 1 },
];