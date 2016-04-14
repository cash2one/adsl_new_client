# -*- coding:utf-8 -*-

import os
import time


class Adsl(object):
    def connect(self):
        try:
            cmdstr = "/sbin/pppoe-start"
            os.system(cmdstr)
        except Exception:
            pass

    def disconnect(self):
        try:
            cmdstr = "/sbin/pppoe-stop"
            os.system(cmdstr)
        except Exception:
            pass

    def reroute(self):
        cmdstr = "ip route del default && ip route add default via 0.0.0.0 dev ppp0"
        os.system(cmdstr)

    def reconnect(self):
        self.disconnect()
        time.sleep(6)
        self.connect()
        self.reroute()
