from abc import ABCMeta, abstractmethod
from SailboatAI.geoutils import Point, Waypoint


class Contest(object):
    __metaclass__ = ABCMeta

    def __init__(self, contest_type):
        self.contest_type = contest_type
        self.waypoints = []

    def load_waypoint_list(self, waypoint_list):
        for waypoint_json in waypoint_list:
            waypoint = Waypoint()
            waypoint.load(waypoint_json)
            self.waypoints.append(waypoint)

    def load_boundary_list(self, boundary_list):
        boundary_list = []
        for boundary_point_json in boundary_list:
            point = Point()
            point.load(boundary_point_json)
            boundary_list.append(point)
        return boundary_list

    @abstractmethod
    def load(self, course_json):
        waypoints = course_json['waypoints']
        self.load_waypoint_list(waypoints)


class FleetRace(Contest):
    def __init__(self, contest_type):
        super(FleetRace, self).__init__(contest_type)
        self.boundary = []
        self.time_to_start = 0

    def load(self, course_json):
        super(FleetRace, self).load(course_json)
        print('course json: %s' % str(course_json))
        self.boundary = self.load_boundary_list(course_json['boundary'])
        #self.time_to_start = course_json['timeToStart']


class StationKeeping(Contest):
    def __init__(self, contest_type):
        super(StationKeeping, self).__init__(contest_type)
        self.time = 0
        self.time_remaining = 0

    def load(self, course_json):
        super(StationKeeping, self).load(course_json)
        self.time = course_json['time']
        self.time_remaining = course_json['timeRemaining']


class AreaScanning(Contest):
    def __init__(self, contest_type):
        super(AreaScanning, self).__init__(contest_type)

    def load(self, course_json):
        super(AreaScanning, self).load(course_json)


class ObstacleAvoidance(Contest):
    def __init__(self, contest_type):
        super(ObstacleAvoidance, self).__init__(contest_type)

    def load(self, course_json):
        super(ObstacleAvoidance, self).load(course_json)


class ContestFactory(object):
    def __init__(self):
        pass

    def load(self, contest_json):
        if 'type' in contest_json:
            contest_type = contest_json['type']
            print('contest type: %s' % contest_type)
            contest = None
            if contest_type == 'fleet-race':
                contest = FleetRace(contest_type)
            elif contest_type == 'station-keeping':
                contest = StationKeeping(contest_type)
            elif contest_type == 'area-scanning':
                contest = AreaScanning(contest_type)
            elif contest_type == 'obstacle-avoidance':
                contest = ObstacleAvoidance(contest_type)
            contest.load(contest_json)
            return contest
        else:
            print('Invalid contest response. Could not find type key.')
            return None