#!/usr/env/python

from __future__ import print_function
import json
from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from SailboatAI.model import Boat

PROXY_IP = 'localhost'
PROXY_PORT = 33330


class WebRemoteClient(Protocol):
    def __init__(self):
        self.uid = ''
        self.seq = 0
        self.boat = Boat()

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
        print(command_data_dict)
        command_json = {'type': 'command',
                        'seq': self.seq,
                        'data': command_data_dict,
                        'uid': self.uid}

        self.send_protocol_msg(command_json)

    def send_move_msg(self, rudder_val, servo_sail):
        move_msg_data = {'action': 'move',
                         'servoRudder': rudder_val,
                         'servoSail': servo_sail}

        self.send_command_msg(move_msg_data)

    def process_register_message(self, register_json):
        self.seq = register_json['seq']
        self.uid = register_json['uid']

    def process_status_message(self, status_json):
        print('process status message')
        print(json.dumps(status_json, sort_keys=True, indent=4))

        status_data_json = status_json['data']
        boat_json = status_data_json['boat']
        self.boat.load(boat_json)
        print(self.boat.gps.latitude)
        print(self.boat.gps.longitude)
        self.send_move_msg(0.4, 0)

    def process_message(self, data):
        message_json = json.loads(str(data).strip())
        message_type = message_json['type']

        if message_type == 'register':
            self.process_register_message(message_json)
        if message_type == 'status':
            self.process_status_message(message_json)

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


def main(reactor):
    factory = WebRemoteClientFactory()
    reactor.connectTCP(PROXY_IP, PROXY_PORT, factory)
    return factory.done


if __name__ == '__main__':
    task.react(main)
