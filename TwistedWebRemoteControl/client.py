import sys
import json
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol


class WebRemoteClient(Protocol):
    def __init__(self):
        self.uid = ''
        self.seq = 0

    def connectionMade(self):
        print('Connected! Sending register message')
        self.send_register_msg(1, 'controller', 'Simulation')

    def send_protocol_msg(self, protocol_json):
        protocol_msg = str(json.dumps(protocol_json)) + '\n'
        self.transport.write(protocol_msg)

    def send_register_msg(self, seq, device_type, channel):
        register_msg_json = {'type': 'register',
                             'seq': seq,
                             'data': {
                                 'deviceType': device_type,
                                 'channel': channel
                             }}

        self.send_protocol_msg(register_msg_json)

    def send_command_msg(self, command_data_dict):
        command_json = {'type': 'command',
                        'seq': self.seq,
                        'data': command_data_dict,
                        'uid': self.uid}

        self.send_protocol_msg(command_json)

    def process_register_message(self, register_json):
        self.seq = register_json['seq']
        self.uid = register_json['uid']

    def process_status_message(self, status_data_json):
        pass

    def process_message(self, data):
        message_json = json.loads(str(data).strip())

        if 'uid' not in message_json or 'type' not in message_json:
            print('Invalid message received: %s' % str(data))
            print('Terminating...')
            sys.exit(-1)

        response_uid = message_json['uid']
        message_type = message_json['type']

        if message_type == 'register' and self.uid == '':
            self.process_register_message(message_json)
        if message_type == 'status' and self.uid == response_uid:
            self.process_status_message(message_json['data'])

    def dataReceived(self, data):
        print('received data...')
        data_lines = data.split('\n')
        for data_line in data_lines:
            if data_line != '':
                self.process_message(data_line)


class WebRemoteClientFactory(ClientFactory):
    protocol = WebRemoteClient

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)
