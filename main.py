#!/usr/env/python

from __future__ import print_function
import json
from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol

PROXY_IP = '192.168.1.43'
PROXY_PORT = 33330


class WebRemoteClient(Protocol):
    def connectionMade(self):
        print('Connected! Sending register message')
        self.send_register_msg()

    def send_register_msg(self):
        register_msg_json = {'type': 'register',
                        'seq': 1,
                        'data': {
                            'deviceType': 'controller',
                            'channel': 'Simulation'
                        }}

        register_msg = str(json.dumps(register_msg_json)) + '\n'
        self.transport.write(register_msg)

    def dataReceived(self, data):
        print('received data...')
        print(data)
        self.transport.loseConnection()


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
