#!/usr/bin/env python
import numpy as np
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from tfpose_ros.msg import Persons, Person, BodyPartElm

# actions = ['nothing', 'stop', 'come on', 'sit down', 'stand up']

#def action_publisher(action_string):
#    pub = rospy.Publisher('/action_recognize', String, queue_size=10)
#    pub.publish(action_string)

def action_publisher(action_id):
    pub = rospy.Publisher('/action_recognize', Int32, queue_size=10)
    pub.publish(action_id)
        # rate.sleep()

def action(human, n):
    # print(human.person_id)

    RShoulder = BodyPartElm()
    RElbow = BodyPartElm()
    RWrist = BodyPartElm()
    LShoulder = BodyPartElm()
    LElbow = BodyPartElm()
    LWrist = BodyPartElm()
    RHip = BodyPartElm()
    LHip = BodyPartElm()
    Neck = BodyPartElm()

    for part in human.body_part:
        if part.part_id == 1:
	    Neck.part_id = part.part_id
            Neck.x = part.x
            Neck.y = part.y
            Neck.confidence = part.confidence
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
        if part.part_id == 8:
            RHip.part_id = part.part_id
            RHip.x = part.x
            RHip.y = part.y
            RHip.confidence = part.confidence
        if part.part_id == 11:
            LHip.part_id = part.part_id
            LHip.x = part.x
            LHip.y = part.y
            LHip.confidence = part.confidence

    print('RShoulder', RShoulder)

    print('RElbow', RElbow)
    print('RWrist', RWrist)

    threshold = 0.3
    #calculation
    # length of the big arm
    R_big_arm_len = np.sqrt((RShoulder.x-RElbow.x)**2 + (RShoulder.y-RElbow.y)**2)
    # R_small_arm_len = np.sqrt((RWrist.x-RElbow.x)**2 + (RWrist.y-RElbow.y)**2)
    R_small_arm_ylen = abs(RWrist.y-RElbow.y)

    L_big_arm_len = np.sqrt((LShoulder.x-LElbow.x)**2 + (LShoulder.y-LElbow.y)**2)
    # L_small_arm_len = np.sqrt((LWrist.x-LElbow.x)**2 + (LWrist.y-LElbow.y)**2)
    L_small_arm_ylen = abs(LWrist.y-LElbow.y)

    # zero pose: Arm dropping
    R_arm_drop = abs(RWrist.y - RHip.y) < 0.2*R_small_arm_ylen and RWrist.confidence > threshold and RHip.confidence > threshold
    L_arm_drop = abs(LWrist.y - LHip.y) < 0.2*L_small_arm_ylen and LWrist.confidence > threshold and LHip.confidence > threshold

    # Action recognize
    if RWrist.y < RShoulder.y and L_arm_drop and (RWrist.confidence > threshold and RShoulder.confidence > threshold):
        action_str = 'come on'
	action_id = 1
    elif LWrist.y < LShoulder.y and R_arm_drop and (LWrist.confidence > threshold and LShoulder.confidence > threshold):
        action_str = 'back'
        action_id = 2

    elif R_small_arm_ylen < R_big_arm_len/3 and L_arm_drop and (RWrist.confidence > threshold and RShoulder.confidence > threshold and RElbow.confidence > threshold):
        action_str = 'stand up'
	action_id = 3

    elif L_small_arm_ylen < L_big_arm_len/3 and R_arm_drop and (LWrist.confidence > threshold and LShoulder.confidence > threshold and LElbow.confidence > threshold):
        action_str = 'sit down'
	action_id = 4

    elif R_small_arm_ylen < R_big_arm_len/3 and L_small_arm_ylen < L_big_arm_len/3 \
        and (RWrist.confidence > threshold and RShoulder.confidence > threshold and RElbow.confidence > threshold) \
        and (LWrist.confidence > threshold and LShoulder.confidence > threshold and LElbow.confidence > threshold):
        action_str = 'stop'
	action_id = 5
    # calibration specific person
    elif RWrist.y < RShoulder.y and LWrist.y < LShoulder.y \
        and RWrist.confidence > threshold and RShoulder.confidence > threshold \
        and LWrist.confidence > threshold and LShoulder.confidence > threshold:
    	action_str = 'calibration'
        action_id = 100
    else:
        action_str = 'do nothing'
	action_id = 0

    # print(action_str+' id:'+str(action_id) + ' human_id:'+str(''))

    return action_id, action_str

def callback(Persons):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    #data = data()
    if(Persons.persons == []):
	# no body
	action_id = 0
        action_publisher(action_id)
        rospy.loginfo('No Body'+' id:'+str(action_id))
    else:
	print('person number: '+str(len(Persons.persons)))
        for human in Persons.persons:
            action_id, action_str = action(human, 0)
	    # mark the action person
            print(action_str+' id:'+str(action_id) + ' current human_id:'+str(Persons.persons.index(human)))
            global actor_id
            if action_id == 100:
                # actor_id = human.person_id
                actor_id = Persons.persons.index(human)

            # Robustness
            global action_temp
            global continue_numOfaction

            if action_id == action_temp and actor_id == Persons.persons.index(human):
                continue_numOfaction += 1
            else:
                action_temp = action_id
                continue_numOfaction = 0
            if continue_numOfaction > 1:
                action_publisher(action_id)
		print('='*20 + action_str + '='*5+'command person id:' + str(actor_id))

def tfpose_listener():

    rospy.init_node('tfpose_listener', anonymous=True)

    rospy.Subscriber("/pose_estimator/pose", Persons, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    global action_temp
    global continue_numOfaction
    action_temp = 0
    continue_numOfaction = 0
    actor_id = 0
    tfpose_listener()
