from SailboatAI.model import Boat, Environment
import math
from SailboatAI.pid import PID
from threading import Timer


class SailboatAIController(object):
    def __init__(self):
        self.boat = Boat()
        self.delta_time = 0
        self.environment = Environment()
        self.is_simulation = False
        self.current_waypoint_idx = 0
        self.pid = PID(1, 0.5, 0.0)
        self.rudder_angle = 0.0
        self.update_timer = Timer()

    def update(self, status_data_json):
        boat_json = status_data_json['boat']
        self.boat.load(boat_json)
        self.delta_time = status_data_json['dt']
        self.environment.load(status_data_json['environment'])
        self.is_simulation = status_data_json['isSimulation']

    def determine_control_output(self, contest):
        rudder_angle = 0
        sail_angle = 0

        self.waypoint = contest.waypoints[self.current_waypoint_idx]

        print("The current waypoint idx is: %s" % str(self.current_waypoint_idx))
        print("My current target is: %s, %s" % (self.waypoint.latitude, self.waypoint.longtitude))

        distance, azimuth = self.boat.gps.point.distance_to(self.waypoint)
        print("I am %s away from the waypoint and the waypoint radius is %s" % (distance, self.waypoint.radius))
        if distance < self.waypoint.radius:
            print('Reached the waypoint!')
            self.waypoint.achieved = True
            self.current_waypoint_idx += 1
            self.waypoint = contest.waypoints[self.current_waypoint_idx]
            distance, azimuth = self.boat.gps.point.distance_to(self.waypoint)

        beta = math.radians(azimuth)
        y = math.pi / 4
        desired_heading = beta - 2 * (y / math.pi) * math.atan(distance / self.waypoint.radius)
        heading = math.radians(self.boat.attitude.heading)
        self.pid.set_target(desired_heading)
        self.pid.update(heading)
        self.rudder_angle += self.pid.output / 1000
        print("desired heading: %s" % str(desired_heading))
        print("heading: %s" % str(heading))
        print("rudder angle: %s" % str(self.rudder_angle))
        return self.rudder_angle, sail_angle