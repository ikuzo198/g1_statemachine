#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ライブラリの読み込み
import rospy
import smach
import smach_ros



class Start(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])

    def execute(self, userdata):
        rospy.loginfo('== Start ==')
        rospy.loginfo('"Good Moring"')
        rospy.sleep(3)
        return 'next'


class Live(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next', 'continue', 'zzz'])
        self.clock = rospy.get_param('~clock')
        self.hungry_flag = rospy.get_param('~hungry_flag')


    def execute(self, userdata):
        # rospy.loginfo('== Live ==')
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
            self.clock = rospy.set_param('~clock')
            return 'continue'
        

class Move2Fridge(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next', 'move2market'])
        self.clock = rospy.get_param('~clock')
        self.dish_counter = rospy.get_param('~dish_counter')

    def execute(self, userdata):
        rospy.loginfo('== Move2Fridge ==')
        rospy.loginfo(f"<< {self.clock} o'clock now >>")
        rospy.loginfo(f'There are {self.dish_counter} foods.')
        rospy.sleep(3)
        
        if self.dish_counter == 0:
            rospy.loginfo(f'I have to go shopping.')
            return 'move2market'
        else:
            return 'next'
        

class Move2Market(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])
        self.dish_counter = rospy.get_param('~dish_counter')
        self.clock = rospy.get_param('~clock')

    def execute(self, userdata):
        rospy.loginfo(f"<< {self.clock} o'clock now >>")
        rospy.loginfo('== Move2Market ==')
        rospy.loginfo("I'll buy foods.")
        rospy.sleep(3)
        self.dish_counter = 5
        self.clock += 1
        return 'next'


class Google(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])

    def execute(self, userdata):
        rospy.loginfo('== OK google. おすすめのランチレシピを教えて．==')
        rospy.sleep(3)
        return 'next'
    

class Cook(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])
        self.dish_counter = rospy.get_param('~dish_counter')
        self.clock = rospy.get_param('~clock')
        print("HERE")

    def execute(self, userdata):
        rospy.loginfo(f"<< {self.clock} o'clock now >>")
        rospy.loginfo('== チーン ==')
        rospy.sleep(3)
        print(self.clock)
        self.clock += 1
        print("hoge:", self.clock)

        self.dish_counter -= 1
        return 'next'
    

class Eat(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['next'])
        self.clock = rospy.get_param('~clock')
        self.hungry_flag = rospy.get_param('~hungry_flag')

    def execute(self, userdata):
        rospy.loginfo(f"<< {self.clock} o'clock now >>")
        rospy.loginfo('== おいしかったぁ ==')
        rospy.sleep(3)
        self.clock += 1
        self.hungry_flag = 0
        return 'next'


def main():
    rospy.init_node('smach_example_state_machine')
    sm = smach.StateMachine(outcomes=['Zzz'])

    with sm:
        smach.StateMachine.add('Start', Start(), 
                               transitions={'next':'Live'})
        smach.StateMachine.add('Live', Live(), 
                               transitions={'next':'Move2Fridge',
                                            'continue':'Live',
                                            'zzz':'Zzz'})
        smach.StateMachine.add('Move2Fridge', Move2Fridge(), 
                               transitions={'next':'Google',
                                            'move2market':'Move2Market'})
        smach.StateMachine.add('Move2Market', Move2Market(), 
                               transitions={'next':'Move2Fridge'})
        smach.StateMachine.add('Google', Google(), 
                               transitions={'next':'Cook'})
        smach.StateMachine.add('Cook', Cook(), 
                               transitions={'next':'Eat'})
        smach.StateMachine.add('Eat', Eat(), 
                               transitions={'next':'Live'})        

    sis = smach_ros.IntrospectionServer("sm_server", sm, "/Born")
    sis.start()
    outcome = sm.execute()
    sis.stop()

if __name__ == '__main__':
    main()