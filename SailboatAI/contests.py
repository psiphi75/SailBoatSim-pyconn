from abc import ABCMeta, abstractmethod


class Waypoint(object):
    def __init__(self, latitude='', longitude='',
                 achieved=False, waypoint_type='circle', radius=0):
        self.latitude = latitude
        self.longitude = longitude
        self.achieved = achieved
        self.type = waypoint_type
        self.radius = radius

    def load(self, waypoint_json):
        self.latitude = waypoint_json['latitude']
        self.longitude = waypoint_json['longitude']
        self.achieved = waypoint_json['achieved']
        self.type = waypoint_json['type']
        self.radius = waypoint_json['radius']


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

    @abstractmethod
    def load(self, course_json):
        waypoints = course_json['waypoints']
        self.load_waypoint_list(waypoints)


class FleetRace(Contest):
    def __init__(self, contest_type):
        super(FleetRace, self).__init__(contest_type)

    def load(self, course_json):
        print('Received course json: %s' % str(course_json['boundary']))


class StationKeeping(Contest):
    def __init__(self, contest_type):
        super(StationKeeping, self).__init__(contest_type)

    def load(self, course_json):
        pass


class AreaScanning(Contest):
    def __init__(self, contest_type):
        super(AreaScanning, self).__init__(contest_type)

    def load(self, course_json):
        pass


class ObstacleAvoidance(Contest):
    def __init__(self, contest_type):
        super(ObstacleAvoidance, self).__init__(contest_type)

    def load(self, course_json):
        pass


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