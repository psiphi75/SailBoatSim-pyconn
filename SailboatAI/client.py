import json
from TwistedWebRemoteControl.client import WebRemoteClient, WebRemoteClientFactory
from SailboatAI.model import Boat, Environment


class SailboatAIClient(WebRemoteClient):
    def __init__(self):
        WebRemoteClient.__init__(self)
        self.boat = Boat()
        self.delta_time = 0
        self.environment = Environment()
        self.is_simulation = False
        self.waypoints = []

    def send_move_msg(self, rudder_val, servo_sail):
        move_msg_data = {'action': 'move',
                         'servoRudder': rudder_val,
                         'servoSail': servo_sail}

        self.send_command_msg(move_msg_data)

    def process_status_message(self, status_data_json):
        print('process status message')
        print(json.dumps(status_data_json, sort_keys=True, indent=4))

        boat_json = status_data_json['boat']
        self.boat.load(boat_json)
        self.delta_time = status_data_json['dt']
        self.environment.load(status_data_json['environment'])
        self.is_simulation = status_data_json['isSimulation']
        self.waypoints = status_data_json['waypoints']

        print(self.boat.gps.latitude)
        print(self.boat.gps.longitude)
        self.send_move_msg(0.4, 0)


class SailboatAIClientFactory(WebRemoteClientFactory):
    protocol = SailboatAIClient
