#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sm_10.srv import GetClock, SetClock, GetClockResponse, SetClockResponse

rospy.init_node('get_clock')
clock_value = rospy.get_param('~clock')

def get_clock(req):
    global clock_value
    response = GetClockResponse()
    response.clock_value = clock_value
    return response

def set_clock(req):
    global clock_value
    clock_value = req.clock_value
    response = SetClockResponse()
    response.success = True
    return response

if __name__ == '__main__':
    get_clock_service = rospy.Service('get_clock', GetClock, get_clock) 
    set_clock_service = rospy.Service('set_clock', SetClock, set_clock) 
    rospy.spin()
