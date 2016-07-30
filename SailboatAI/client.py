import json
from TwistedWebRemoteControl.client import WebRemoteClient, WebRemoteClientFactory
from SailboatAI.controllers import SailboatAIController

SIMULATION_CHANNEL = 'Simulation'
CONTEST_MANAGER_CHANNEL = 'ContestManager'


class SailboatAIClient(WebRemoteClient):
    def __init__(self):
        WebRemoteClient.__init__(self)
        self.boat_ai_controller = SailboatAIController()
        self.add_register_callback(SIMULATION_CHANNEL, self.process_simulation_register_message)
        self.add_message_callback(SIMULATION_CHANNEL, 'status', self.process_simulation_status_message)
        self.add_register_callback(CONTEST_MANAGER_CHANNEL, self.process_contest_manager_register_message)
        self.add_message_callback(CONTEST_MANAGER_CHANNEL, 'status', self.process_contest_manager_status_message)

    def connectionMade(self):
        super(SailboatAIClient, self).connectionMade()
        self.send_register_msg(1, 'controller', 'Simulation')
        self.send_register_msg(1, 'controller', 'ContestManager')

    def process_simulation_register_message(self, uid, register_json):
        pass

    def process_contest_manager_register_message(self, uid, register_json):
        self.send_contest_request('fleet-race', 'viana-do-castelo', False)
        print('Send contest manager register')

    def send_move_msg(self, rudder_val, servo_sail):
        move_msg_data = {'action': 'move',
                         'servoRudder': rudder_val,
                         'servoSail': servo_sail}

        self.send_command_msg(SIMULATION_CHANNEL, move_msg_data)

    def send_contest_request(self, type, location, realtime):
        request_contest_data = {'action': 'request-contest',
                                'type': type,
                                'location': location,
                                'realtime': realtime}

        self.send_command_msg(CONTEST_MANAGER_CHANNEL, request_contest_data)

    def process_simulation_status_message(self, uid, message_json):
        print('process simulation status message')
        status_data_json = message_json['data']
        self.boat_ai_controller.update(status_data_json)
        self.send_move_msg(0.4, 0)

    def process_contest_manager_status_message(self, uid, message_json):
        print('Status received for course: %s' % str(message_json))


class SailboatAIClientFactory(WebRemoteClientFactory):
    protocol = SailboatAIClient
