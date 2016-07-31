import json
from TwistedWebRemoteControl.client import WebRemoteClient, WebRemoteClientFactory
from SailboatAI.controllers import SailboatAIController


class SailboatAIClient(WebRemoteClient):
    def __init__(self):
        WebRemoteClient.__init__(self)
        self.settings = None
        self.boat_ai_controller = SailboatAIController()

    def connectionMade(self):
        super(SailboatAIClient, self).connectionMade()
        self.add_register_callback(self.settings.toy_channel, self.process_toy_register_message)
        self.add_message_callback(self.settings.toy_channel, 'status', self.process_toy_status_message)
        self.add_register_callback(self.settings.contest_manager_channel, self.process_contest_manager_register_message)
        self.add_message_callback(self.settings.contest_manager_channel, 'status', self.process_contest_manager_status_message)
        self.send_register_msg(1, 'controller', self.settings.toy_channel)
        self.send_register_msg(1, 'controller', self.settings.contest_manager_channel)

    def process_toy_register_message(self, uid, register_json):
        pass

    def process_contest_manager_register_message(self, uid, register_json):
        self.send_contest_request(self.settings.type, self.settings.location, self.settings.realtime)
        print('Send contest manager register')

    def send_move_msg(self, rudder_val, servo_sail):
        move_msg_data = {'action': 'move',
                         'servoRudder': rudder_val,
                         'servoSail': servo_sail}

        self.send_command_msg(self.settings.toy_channel, move_msg_data)

    def send_contest_request(self, type, location, realtime):
        request_contest_data = {'action': 'request-contest',
                                'type': type,
                                'location': location,
                                'realtime': realtime}

        self.send_command_msg(self.settings.contest_manager_channel, request_contest_data)

    def process_toy_status_message(self, uid, message_json):
        print('process simulation status message')
        status_data_json = message_json['data']
        self.boat_ai_controller.update(status_data_json)
        self.send_move_msg(0.4, 0)

    def process_contest_manager_status_message(self, uid, message_json):
        print('Status received for course: %s' % str(message_json))


class SailboatAIClientFactory(WebRemoteClientFactory):
    protocol = SailboatAIClient

    def __init__(self, settings):
        super(SailboatAIClientFactory, self).__init__()
        self.settings = settings

    def buildProtocol(self, addr):
        client = super(WebRemoteClientFactory, self).buildProtocol(addr)
        client.settings = self.settings
        return client
