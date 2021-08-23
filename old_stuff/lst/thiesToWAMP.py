"""
Created on 22.02.2017

Topic:  wetter.thies
RPCs:   (keine)

@author: florian fiebig 
"""

import sys
import traceback
import time
from base64 import b64encode

from twisted.internet.defer import inlineCallbacks, returnValue
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet import task
from time import time

wampRouterAddress = u"wss://smarthome.aifb.kit.edu:8888/ws"
wampRouterRealm = u"eshl"
wampTopic = u"ieh.weather.thies"

session = None

class WampThiesWeather(ApplicationSession):
    """Interface between the WAMP and the Thies weather station"""

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)

    def publishLoop(self):
        print('publishing on {}'.format(wampTopic))
        timestamp = int(time())
        self.publish(wampTopic,{'timestamp': timestamp, 'temperature': 20, 'windspeed': 15})

    def onJoin(self, details):
        ApplicationSession.onJoin(self, details)
        session = self
        self._loop = task.LoopingCall(self.publishLoop)
        self._loop.start(1.0)

        print("session ready")

    def onLeave(self, details):
        ApplicationSession.onLeave(self, details)
        session = None
        print("leaving")

if __name__ == '__main__':
    creds = b'thies:bS6NDHdszwwEIkMTMhMEjuLKqqXsI8F0'
    headers = {'Authorization': 'Basic ' + b64encode(creds).decode()}
    runner = ApplicationRunner(url=wampRouterAddress, realm=wampRouterRealm, headers=headers)
    runner.run(WampThiesWeather, auto_reconnect=True)