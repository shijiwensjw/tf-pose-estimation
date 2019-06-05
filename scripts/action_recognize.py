#!/usr/bin/env python
import numpy as np
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from tfpose_ros.msg import Persons, Person, BodyPartElm

# actions = ['nothing', 'stop', 'come on', 'sit down', 'stand up']

def action_publisher(action_string):
    pub = rospy.Publisher('/action_recognize', String, queue_size=10)
    pub.publish(action_string)
        # rate.sleep()

def action(human, n):
    # print(human.person_id)
    # print('-----------------')
    # print(type(human.body_part))
    # print(len(human.body_part))
    # print('-----------------')
    # print(type(human.body_part[1]))
    # l=np.array(human.body_part)
    # print('shape', l.shape)

    RShoulder = BodyPartElm()
    RElbow = BodyPartElm()
    RWrist = BodyPartElm()
    LShoulder = BodyPartElm()
    LElbow = BodyPartElm()
    LWrist = BodyPartElm()

    for part in human.body_part:
        # body right
        if part.part_id == 2:
            RShoulder.part_id = part.part_id
            RShoulder.x = part.x
            RShoulder.y = part.y
            RShoulder.confidence = part.confidence
        if part.part_id == 3:
            RElbow.part_id = part.part_id
            RElbow.x = part.x
            RElbow.y = part.y
            RElbow.confidence = part.confidence
        if part.part_id == 4:
            RWrist.part_id = part.part_id
            RWrist.x = part.x
            RWrist.y = part.y
            RWrist.confidence = part.confidence
        # body left
        if part.part_id == 5:
            LShoulder.part_id = part.part_id
            LShoulder.x = part.x
            LShoulder.y = part.y
            LShoulder.confidence = part.confidence
        if part.part_id == 6:
            LElbow.part_id = part.part_id
            LElbow.x = part.x
            LElbow.y = part.y
            LElbow.confidence = part.confidence
        if part.part_id == 7:
            LWrist.part_id = part.part_id
            LWrist.x = part.x
            LWrist.y = part.y
            LWrist.confidence = part.confidence

    print('RShoulder', RShoulder)

    print('RElbow', RElbow)
    print('RWrist', RWrist)

    threshold = 0.5
    #calculation
    # length of the big arm
    R_big_arm_len = np.sqrt((RShoulder.x-RElbow.x)**2 + (RShoulder.y-RElbow.y)**2)
    # R_small_arm_len = np.sqrt((RWrist.x-RElbow.x)**2 + (RWrist.y-RElbow.y)**2)
    R_small_arm_ylen = abs(RWrist.y-RElbow.y)

    L_big_arm_len = np.sqrt((LShoulder.x-LElbow.x)**2 + (LShoulder.y-LElbow.y)**2)
    # L_small_arm_len = np.sqrt((LWrist.x-LElbow.x)**2 + (LWrist.y-LElbow.y)**2)
    L_small_arm_ylen = abs(LWrist.y-LElbow.y)

    # Action recognize
    if RWrist.y < RShoulder.y and (RWrist.confidence > threshold and RShoulder.confidence > threshold):
        action_str = 'come on'
    elif R_small_arm_ylen < R_big_arm_len/3 and (RWrist.confidence > threshold and RShoulder.confidence > threshold and RElbow.confidence > threshold):
        action_str = 'sit down'

    elif LWrist.y < LShoulder.y and (LWrist.confidence > threshold and LShoulder.confidence > threshold):
        action_str = 'stand up'
    elif L_small_arm_ylen < L_big_arm_len/3 and (LWrist.confidence > threshold and LShoulder.confidence > threshold and LElbow.confidence > threshold):
        action_str = 'stop'
    else:
        action_str = 'do nothing'

    print(action_str)

    # last = ''
    # if last == action_str and action_str != 'do nothing':
    #     n += 1
    # else:
    #     n = 0
    # last = action_str
    #
    # if n > 3:
    #     action_publisher(action_str)
    action_publisher(action_str)


def callback(Persons):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    #data = data()
    if(Persons.persons == []):
        rospy.loginfo('No Body')
    else:
        for human in Persons.persons:
            action(human, 0)
    # print(Persons.persons[0].person_id)
    # print(data.image_w)

def tfpose_listener():

    rospy.init_node('tfpose_listener', anonymous=True)

    #rospy.Subscriber("/pose_estimator/pose", Persons, callback)
    rospy.Subscriber("/pose_estimator/pose", Persons, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    tfpose_listener()
