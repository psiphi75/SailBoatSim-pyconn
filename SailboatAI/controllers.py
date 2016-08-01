from SailboatAI.model import Boat, Environment


class SailboatAIController(object):
    def __init__(self):
        self.boat = Boat()
        self.delta_time = 0
        self.environment = Environment()
        self.is_simulation = False
        self.current_waypoint_idx = 0

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

        print(self.boat.gps.point.distance_to(self.waypoint))

        return rudder_angle, sail_angle