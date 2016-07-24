import json


class Settings(object):
    def __init__(self):
        self.proxy_ip = ''
        self.proxy_port = 0

    def load(self, json_file_path):
        settings_file = open(json_file_path, 'r')
        settings_text = settings_file.read()
        settings_json = json.loads(settings_text)
        settings_file.close()
        self.proxy_ip = settings_json['proxy_ip']
        self.proxy_port = settings_json['proxy_port']