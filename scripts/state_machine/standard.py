#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ライブラリの読み込み
import rospy
import smach
import smach_ros
from std_msgs.msg import Int32

class Start(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])

    def execute(self, userdata):
        rospy.loginfo('== Start ==')
        rospy.loginfo('"Good Moring"')
        rospy.sleep(3)
        return 'next'
    
