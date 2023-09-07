#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ライブラリの読み込み
import rospy
import smach
import smach_ros
from g1_statemachine.srv import GetClock, SetClock

class Eat(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])
        self.clock = None
        self.hungry_flag = None

    def execute(self, userdata):
        try:
            self.get_clock = rospy.ServiceProxy('get_clock', GetClock)
            self.set_clock = rospy.ServiceProxy('set_clock', SetClock)
            response = self.get_clock()
            self.clock = response.clock_value
        
            rospy.loginfo(f"<< {self.clock} o'clock now >>")
            rospy.loginfo('== おいしかったぁ ==')
            rospy.sleep(3)

            self.clock += 1
            self.hungry_flag = 0

            self.set_clock(self.clock)

            return 'next'
        
        except rospy.ServiceException as e:
            rospy.logerr("ROSサービスの呼び出しに失敗しました: %s", str(e))
            return 'next'  # エラー時の適切な処理を追加