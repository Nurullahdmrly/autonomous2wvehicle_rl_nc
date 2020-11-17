#!/usr/bin/env python
#-*-coding: utf-8 -*-

import rospy
from nav_msgs.msg import Odometry  #"""rosmsg show Odometry we see"""
from tf.transformations import euler_from_quaternion #"""robotun dönel hareketi için gerekli """
from geometry_msgs.msg import Point , Twist #""" position için hedef uzantı"""
from math import atan2
x = 0.0
y = 0.0
theta = 0.0

def newOdom (msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation #"""robotun dönel hareketi orientation euler tabanlı olduğundan 4 değişkeni buna tanımlıyoruz"""
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])



rospy.init_node ("speed_controller")

sub = rospy.Subscriber("/odometry/filtered_map",Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel",Twist, queue_size=1)

speed = Twist()

r = rospy.Rate(4) #4 hz

goal = Point ()
goal.x = 2
goal.y = 2


while not rospy.is_shutdown():
    inc_x = goal.x - x
    inc_y = goal.y - y

    angle_to_goal = atan2 (inc_y, inc_x)

    if abs(angle_to_goal - theta) > 0.1:  #"""abs mutlak değer"""
        speed.linear.x = 0.0
        speed.angular.z = 0.3
    else:
        speed.linear.x = 0.5
        speed.angular.z = 0.0

    pub.publish(speed)
    r.sleep()
    print(abs(angle_to_goal - theta), angle_to_goal , theta)
    print(x , y)
