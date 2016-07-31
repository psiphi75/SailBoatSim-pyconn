import json


class Settings(object):
    def __init__(self):
        self.proxy_ip = ''
        self.proxy_port = 0
        self.toy_channel = ''
        self.contest_manager_channel = ''
        self.type = ''
        self.location = ''
        self.realtime = False

    def load(self, json_file_path):
        settings_file = open(json_file_path, 'r')
        settings_text = settings_file.read()
        settings_json = json.loads(settings_text)
        settings_file.close()
        self.proxy_ip = settings_json['proxy_ip']
        self.proxy_port = settings_json['proxy_port']
        self.toy_channel = settings_json['toy_channel']
        self.contest_manager_channel = settings_json['contest_manager_channel']
        race_settings = settings_json['race']
        self.type = race_settings['type']
        self.location = race_settings['location']
        self.realtime = race_settings['realtime']