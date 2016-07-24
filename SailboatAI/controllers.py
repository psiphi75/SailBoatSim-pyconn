from SailboatAI.model import Boat, Environment


class SailboatAIController(object):
    def __init__(self):
        self.boat = Boat()
        self.delta_time = 0
        self.environment = Environment()
        self.is_simulation = False
        self.waypoints = []

    def update(self, status_data_json):
        boat_json = status_data_json['boat']
        self.boat.load(boat_json)
        self.delta_time = status_data_json['dt']
        self.environment.load(status_data_json['environment'])
        self.is_simulation = status_data_json['isSimulation']
        self.waypoints = status_data_json['waypoints']

    def determine_control_output(self):
        pass