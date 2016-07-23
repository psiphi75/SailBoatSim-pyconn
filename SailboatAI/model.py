
class ApparentWind(object):
    def __init__(self):
        self.heading = 0
        self.heading_to_boat = 0
        self.speed = 0

    def load(self, apparent_wind_json):
        self.heading = apparent_wind_json['heading']
        self.heading_to_boat = apparent_wind_json['headingToBoat']
        self.speed = apparent_wind_json['speed']


class Attitude(object):
    def __init__(self):
        self.heading = 0
        self.pitch = 0
        self.roll = 0

    def load(self, attitude_json):
        self.heading = attitude_json['heading']
        self.pitch = attitude_json['pitch']
        self.roll = attitude_json['roll']


class GPS(object):
    def __init__(self):
        self.latitude = 0
        self.longitude = 0

    def load(self, gps_json):
        self.latitude = gps_json['latitude']
        self.longitude = gps_json['longitude']


class Servos(object):
    def __init__(self):
        self.has_rudder = False
        self.has_sail = False

    def load(self, servos_json):
        self.has_rudder = servos_json['rudder']
        self.has_sail = servos_json['sail']


class Velocity(object):
    def __init__(self):
        self.direction = 0
        self.speed = 0

    def load(self, velocity_json):
        self.direction = velocity_json['direction']
        self.speed = velocity_json['speed']


class Boat(object):
    def __init__(self):
        self.apparent_wind = ApparentWind()
        self.attitude = Attitude()
        self.gps = GPS()
        self.servos = Servos()
        self.velocity = Velocity()

    def load(self, boat_json):
        self.apparent_wind.load(boat_json['apparentWind'])
        self.attitude.load(boat_json['attitude'])
        self.gps.load(boat_json['gps'])
        self.servos.load(boat_json['servos'])
        self.velocity.load(boat_json['velocity'])