#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ライブラリの読み込み
import rospy
import smach
import smach_ros

class Google(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])

    def execute(self, userdata):
        rospy.loginfo('== OK google. おすすめのランチレシピを教えて．==')
        rospy.sleep(3)
        return 'next'
    