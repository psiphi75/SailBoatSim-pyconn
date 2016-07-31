#!/usr/env/python

from __future__ import print_function
import os
from twisted.internet import task
from SailboatAI.client import SailboatAIClientFactory
from SailboatAI.settings import Settings


def main(reactor):
    settings = Settings()
    settings_file_path = os.path.join(os.getcwd(), 'settings.json')
    settings.load(settings_file_path)
    factory = SailboatAIClientFactory(settings)
    reactor.connectTCP(settings.proxy_ip, settings.proxy_port, factory)
    return factory.done

if __name__ == '__main__':
    task.react(main)
