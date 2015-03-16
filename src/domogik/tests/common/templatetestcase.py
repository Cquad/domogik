#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Purpose
=======

Tools for regression tests

Usage
=====

@author: bibi21000 <sgallet@gmail.com>     # original functions
         Fritz SMH <fritz.smh@gmail.com>   # adaptation as a generic library
@copyright: (C) 2007-2012 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

import datetime
from threading import Event
from domogik.xpl.common.xplconnector import Listener
from domogik.xpl.common.xplmessage import XplMessage
from domogik.xpl.common.plugin import XplPlugin
from domogik.tests.common.helpers import *
import unittest
import time

class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        """ sort of a Constructor
        """
        print(u"\n------------------------------------------------------------------")
        #self.config = {}


    ### xpl tools

    def wait_for_xpl(self, xpltype = None, xplschema = None, xplsource = None, data = {}, timeout = 10):
        """ Wait for a xpl message for a given time (in seconds)
            @param xpltype: the xpl message type. Possible values are None (all), xpl-cmnd, xpl-stat, xpl-trig
            @param xplschema : the xpl schema (sensor.basic for example)
            @param xplsource : the xpl source of the message
            @param data : the list of keys/values we should find in the message. { 'key1' : 'val1', ... }
            @param timeout : time (in seconds) given to get the message. Once timeout has expired, we return False
        """

        # create the listener to catch the message
        self._xpl_received = Event()
        criteria = {'schema': xplschema,
                    'xpltype': xpltype,
                    'xplsource': xplsource}
        for key in data:
            criteria[key] = str(data[key])
        listener = Listener(self._wait_for_xpl_cb, 
                            self.myxpl, 
                            criteria)

        # we add 5% to the timeout as some operations may be done in the plugin and so the interval is not totally exact
        timeout = timeout*1.05 
        self._xpl_received.wait(timeout)
        if not self._xpl_received.is_set():
            raise RuntimeError("No xPL message received")
        print(u"xPL message received : {0}".format(self.xpl_data))
        # remove the listener
        listener.unregister()
        return True
       


    def _wait_for_xpl_cb(self, message):
        """ Callback for the listener created in wait_for_xpl
            @param message : xpl message received
        """
        self._xpl_received.set()
        self.xpl_data = message
    

    ### time tools

    def is_interval_of(self, interval, delta_to_check):
        """ Check if the delta_to_check corresponds to the interval (5% margin)
            @param interval : in seconds
            @param delta_to_check : interval required (difference of 2 datatime.now()
        """
        delta_seconds = delta_to_check.total_seconds()
        print(u"Compare the delta of {0} seconds to the required interval of {1} seconds".format(delta_seconds, interval))
        diff = abs(delta_seconds - interval)
        five_percent_of_interval = 0.05 * interval
        if diff > five_percent_of_interval:
            raise RuntimeError("There is a difference of {0} seconds between the required interval and the measured time. This is more than 5% of the required interval (5% = {1} seconds)".format(diff, five_percent_of_interval))
        else:
            print(u"There is a difference of {0} seconds between the required interval and the measured time. This is less than 5% of the required interval (5% = {1} seconds)".format(diff, five_percent_of_interval))
            return True



