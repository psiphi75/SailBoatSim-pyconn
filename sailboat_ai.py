#!/usr/env/python

from __future__ import print_function
import sys
import json
from twisted.internet import task
from SailboatAI.client import SailboatAIClientFactory

PROXY_IP = '192.168.1.42'
PROXY_PORT = 33330


def main(reactor):
    factory = SailboatAIClientFactory()
    reactor.connectTCP(PROXY_IP, PROXY_PORT, factory)
    return factory.done


if __name__ == '__main__':
    task.react(main)
