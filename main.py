#!/usr/env/python

from __future__ import print_function
import json
from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol

PROXY_IP = 'localhost'
PROXY_PORT = 33330


class ApparentWind(object):
    def __init__(self, heading, heading_to_boat, roll):
        self.heading = heading
        self.heading_to_boat = heading_to_boat
        self.roll = roll


class Attitude(object):
    def __init__(self, heading, pitch, roll):
        self.heading = heading
        self.pitch = pitch
        self.roll = roll


class GPS(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class Servos(object):
    def __init__(self, has_rudder, has_sail):
        self.has_rudder = has_rudder
        self.has_sail = has_sail


class Velocity(object):
    def __init__(self, direction, speed):
        self.direction = direction
        self.speed = speed


class Boat(object):
    def __init__(self, apparent_wind, attitude, gps, servos, velocity):
        self.apparent_wind = apparent_wind
        self.attitude = attitude
        self.gps = gps
        self.servos = servos
        self.velocity = velocity


class JSONBoatFactory(object):

    @staticmethod
    def load_apparent_wind(apparent_wind_json):
        print('apprent wind json: %s' % str(apparent_wind_json))
        heading = apparent_wind_json['heading']
        heading_to_boat = apparent_wind_json['headingToBoat']
        speed = apparent_wind_json['speed']
        return ApparentWind(heading, heading_to_boat, speed)

    @staticmethod
    def load_attitude(attitude_json):
        heading = attitude_json['heading']
        pitch = attitude_json['pitch']
        roll = attitude_json['roll']
        return Attitude(heading, pitch, roll)

    @staticmethod
    def load_gps(gps_json):
        latitude = gps_json['latitude']
        longitude = gps_json['longitude']
        return GPS(latitude, longitude)

    @staticmethod
    def load_servos(servos_json):
        has_rudder = servos_json['rudder']
        has_sail = servos_json['sail']
        return Servos(has_rudder, has_sail)

    @staticmethod
    def load_velocity(velocity_json):
        direction = velocity_json['direction']
        speed = velocity_json['speed']
        return Velocity(direction, speed)

    @staticmethod
    def load(boat_json):
        apparent_wind = JSONBoatFactory.load_apparent_wind(boat_json['apparentWind'])
        attitude = JSONBoatFactory.load_attitude(boat_json['attitude'])
        gps = JSONBoatFactory.load_gps(boat_json['gps'])
        servos = JSONBoatFactory.load_servos(boat_json['servos'])
        velocity = JSONBoatFactory.load_velocity(boat_json['velocity'])

        return Boat(apparent_wind, attitude, gps, servos, velocity)


class WebRemoteClient(Protocol):
    def __init__(self):
        self.uid = ''
        self.seq = 0

    def connectionMade(self):
        print('Connected! Sending register message')
        self.send_register_msg(1, 'controller', 'Simulation')

    def send_register_msg(self, seq, device_type, channel):
        register_msg_json = {'type': 'register',
                             'seq': seq,
                             'data': {
                                 'deviceType': device_type,
                                 'channel': channel
                             }}

        register_msg = str(json.dumps(register_msg_json)) + '\n'
        self.transport.write(register_msg)

    def process_register_message(self, register_json):
        self.seq = register_json['seq']
        self.uid = register_json['uid']

    def process_status_message(self, status_json):
        print('process status message')
        print(json.dumps(status_json, sort_keys=True, indent=4))

        status_data_json = status_json['data']
        boat_json = status_data_json['boat']
        boat = JSONBoatFactory.load(boat_json)
        print(boat.velocity.direction)

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
