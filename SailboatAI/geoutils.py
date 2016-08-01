import math
from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84


class Point(object):
    def __init__(self, latitude='', longitude=''):
        self.latitude = latitude
        self.longtitude = longitude

    def load(self, point_json):
        self.latitude = point_json['latitude']
        self.longtitude = point_json['longitude']

    def distance_to(self, point):
        azrange = geod.Inverse(self.latitude, self.longtitude, point.latitude, point.longtitude)
        return azrange['s12'], azrange['azi2']


class Waypoint(Point):
    def __init__(self, latitude='', longitude='',
                 achieved=False, waypoint_type='circle', radius=0):
        super(Waypoint, self).__init__(latitude, longitude)
        self.achieved = achieved
        self.type = waypoint_type
        self.radius = radius

    def load(self, waypoint_json):
        super(Waypoint, self).load(waypoint_json)
        self.achieved = waypoint_json['achieved']
        self.type = waypoint_json['type']
        self.radius = waypoint_json['radius']