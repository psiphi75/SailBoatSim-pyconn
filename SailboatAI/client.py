import json
from TwistedWebRemoteControl.client import WebRemoteClient, WebRemoteClientFactory
from SailboatAI.controllers import SailboatAIController

SIMULATION_SEQ = 1
CONTEST_MANAGER_SEQ = 2


class SailboatAIClient(WebRemoteClient):
    def __init__(self):
        WebRemoteClient.__init__(self)
        self.boat_ai_controller = SailboatAIController()
        self.register_msg('status', self.process_status_message)

    def connectionMade(self):
        super(SailboatAIClient, self).connectionMade()
        self.send_register_msg(SIMULATION_SEQ, 'controller', 'Simulation')
        self.send_register_msg(CONTEST_MANAGER_SEQ, 'controller', 'ContestManager')

    def process_register_message(self, uid, register_json):
        super(SailboatAIClient, self).process_register_message(uid, register_json)
        print(self.uids)
        if CONTEST_MANAGER_SEQ in self.uids and uid == self.uids[CONTEST_MANAGER_SEQ]:
            self.send_contest_request('fleet-race', 'viana-do-castelo', False)
            print('Send contest manager register')

    def send_move_msg(self, rudder_val, servo_sail):
        move_msg_data = {'action': 'move',
                         'servoRudder': rudder_val,
                         'servoSail': servo_sail}

        self.send_command_msg(SIMULATION_SEQ, move_msg_data)

    def send_contest_request(self, type, location, realtime):
        request_contest_data = {'action': 'request-contest',
                                'type': type,
                                'location': location,
                                'realtime': realtime}

        self.send_command_msg(CONTEST_MANAGER_SEQ, request_contest_data)

    def process_status_message(self, uid, message_json):
        print('process status message')
        if uid == self.uids[SIMULATION_SEQ]:
            status_data_json = message_json['data']
            #print(json.dumps(status_data_json, sort_keys=True, indent=4))
            self.boat_ai_controller.update(status_data_json)
            self.send_move_msg(0.4, 0)
        elif uid == self.uids[CONTEST_MANAGER_SEQ]:
            print('Status received four course: %s' % str(message_json))


class SailboatAIClientFactory(WebRemoteClientFactory):
    protocol = SailboatAIClient
