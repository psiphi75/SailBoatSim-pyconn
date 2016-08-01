import sys
import json
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol


class WebRemoteClient(Protocol, object):
    def __init__(self):
        self.message_data = ''
        self.message_continues = False
        self.uids = {}
        self.register_callbacks = {}
        self.message_callbacks = {}
        self.add_message_callback(None, 'register', self.process_register_message)

    def connectionMade(self):
        print('Connected! Sending register message')

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

    def send_command_msg(self, channel_name, command_data_dict):
        if channel_name in self.uids:
            command_json = {'type': 'command',
                            'seq': 1,
                            'data': command_data_dict,
                            'uid': self.uids[channel_name]}

            self.send_protocol_msg(command_json)

    def process_register_message(self, uid, register_json):
        print('Received register for %s' % (register_json))
        register_seq = register_json['seq']
        register_uid = register_json['uid']
        register_channel = register_json['data']['channel']
        self.uids[register_channel] = register_uid
        print('Received register on %s %s' % (register_seq, register_uid))
        self.register_callbacks[register_channel](uid, register_json)

    def add_message_callback(self, channel_name, msg_id, callback):
        message_key = (channel_name, msg_id)
        self.message_callbacks[message_key] = callback

    def add_register_callback(self, channel_name, callback):
        self.register_callbacks[channel_name] = callback

    def find_channel_name(self, uid):
        for channel_name in self.uids:
            channel_uid = self.uids[channel_name]
            if uid == channel_uid:
                return channel_name

    def process_message(self, data):
        self.message_data += data
        try:
            message_json = json.loads(str(self.message_data).strip())
            self.message_continues = False
        except ValueError:
            self.message_continues = True

        if self.message_continues:
            return
        else:
            self.message_data = ''

        if 'uid' not in message_json or 'type' not in message_json:
            print('Invalid message received: %s' % str(data))
            print('Terminating...')
            sys.exit(-1)

        response_uid = message_json['uid']
        message_type = message_json['type']

        channel_name = self.find_channel_name(response_uid)

        message_key = (channel_name, message_type)
        if message_key in self.message_callbacks:
            msg_callback = self.message_callbacks[message_key]
            msg_callback(response_uid, message_json)
        else:
            print('Received unregistered message: %s' % message_type)

    def dataReceived(self, data):
        print('received data...')
        data_lines = data.split('\n')
        for data_line in data_lines:
            if data_line != '':
                self.process_message(data_line)


class WebRemoteClientFactory(ClientFactory, object):
    protocol = WebRemoteClient

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)
