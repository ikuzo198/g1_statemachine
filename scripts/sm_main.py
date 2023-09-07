#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ライブラリの読み込み
import rospy
import smach
import smach_ros
import os

from state_machine import (
    standard,
    live,
    move2fridge,
    move2market,
    google,
    cook,
    eat
)


class StateMachine(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])

        self.sm = smach.StateMachine(outcomes=['Zzz'])

        with self.sm:
            smach.StateMachine.add('Start', standard.Start(), 
                                transitions={'next':'Live'})
            smach.StateMachine.add('Live', live.Live(), 
                                transitions={'next':'Move2Fridge',
                                                'continue':'Live',
                                                'zzz':'Zzz'})
            smach.StateMachine.add('Move2Fridge', move2fridge.Move2Fridge(), 
                                transitions={'next':'Google',
                                                'move2market':'Move2Market'})
            smach.StateMachine.add('Move2Market', move2market.Move2Market(), 
                                transitions={'next':'Move2Fridge'})
            smach.StateMachine.add('Google', google.Google(), 
                                transitions={'next':'Cook'})
            smach.StateMachine.add('Cook', cook.Cook(), 
                                transitions={'next':'Eat'})
            smach.StateMachine.add('Eat', eat.Eat(), 
                                transitions={'next':'Live'})        

        sis = smach_ros.IntrospectionServer("sm_server", self.sm, "/Born")
        sis.start()
        outcome = self.sm.execute()
        sis.stop()


    def delete(self) -> None:
        del self.sm

    def run(self) -> None:
        self.sm.execute()


def main():
    rospy.init_node(os.path.basename(__file__).split(".")[0])

    cls = StateMachine()
    rospy.on_shutdown(cls.delete)
    try:
        cls.run()
    except rospy.exceptions.ROSException as e:
        rospy.logerr("[" + rospy.get_name() + "]: FAILURE")
        rospy.logerr("[" + rospy.get_name() + "]: " + str(e))


if __name__ == '__main__':
    main()