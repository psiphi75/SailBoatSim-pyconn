import json
from TwistedWebRemoteControl.client import WebRemoteClient, WebRemoteClientFactory
from SailboatAI.controllers import SailboatAIController


class SailboatAIClient(WebRemoteClient):
    def __init__(self):
        WebRemoteClient.__init__(self)
        self.boat_ai_controller = SailboatAIController()

    def send_move_msg(self, rudder_val, servo_sail):
        move_msg_data = {'action': 'move',
                         'servoRudder': rudder_val,
                         'servoSail': servo_sail}

        self.send_command_msg(move_msg_data)

    def process_status_message(self, status_data_json):
        print('process status message')
        print(json.dumps(status_data_json, sort_keys=True, indent=4))
        self.boat_ai_controller.update(status_data_json)
        self.send_move_msg(0.4, 0)


class SailboatAIClientFactory(WebRemoteClientFactory):
    protocol = SailboatAIClient
