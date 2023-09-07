#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ライブラリの読み込み
import rospy
import smach
import smach_ros
from g1_statemachine.srv import GetClock, SetClock

class Live(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next', 'continue', 'zzz'])
        self.hubgry_flag = None
        self.clock = None

    def execute(self, userdata):
        try:
            rospy.wait_for_service('get_clock') 
            rospy.wait_for_service('set_clock') 
            self.get_clock = rospy.ServiceProxy('get_clock', GetClock)
            self.set_clock = rospy.ServiceProxy('set_clock', SetClock)
            response = self.get_clock()
            self.clock = response.clock_value
            rospy.loginfo(f"<< {self.clock} o'clock now >>")
            rospy.sleep(3)

            if (self.clock == 8
                    or self.clock == 12
                    or self.clock == 20):
                self.hungry_flag = 1
                return 'next'
            
            elif self.clock == 24:
                rospy.loginfo("Zzz...")
                return 'zzz'
            
            else:
                self.clock += 1
                rospy.loginfo(f"Current clock value: {self.clock}")

                self.set_clock(self.clock)
                return 'continue'

        except rospy.ServiceException as e:
            rospy.logerr("ROSサービスの呼び出しに失敗しました: %s", str(e))
            return 'next'  # エラー時の適切な処理を追加