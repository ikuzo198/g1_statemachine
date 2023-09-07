#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ライブラリの読み込み
import rospy
import smach
import smach_ros
from sm_10.srv import GetClock, SetClock

class Move2Fridge(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next', 'move2market'])
        self.dish_counter = None
        self.clock = None

    def execute(self, userdata):
        try:
            self.get_clock = rospy.ServiceProxy('get_clock', GetClock)
            self.set_clock = rospy.ServiceProxy('set_clock', SetClock)
            response = self.get_clock()
            self.clock = response.clock_value

            rospy.loginfo('== Move2Fridge ==')
            rospy.loginfo(f"<< {self.clock} o'clock now >>")
            rospy.loginfo(f'There are {self.dish_counter} foods.')
            rospy.sleep(3)

            if self.dish_counter == 0:
                rospy.loginfo(f'I have to go shopping.')
                return 'move2market'
            else:
                return 'next'

        except rospy.ServiceException as e:
            rospy.logerr("ROSサービスの呼び出しに失敗しました: %s", str(e))
            return 'next'  # エラー時の適切な処理を追加
