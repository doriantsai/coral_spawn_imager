#! /usr/bin/env python3

"""
project: coral_spawn_imager 
file: simple publisher
A ROS node that publishes words from HQ picam at set intervals
author: Dorian Tsai
email: dorian.tsai@gmail.com
date: 2022/Oct/07
"""

import rospy
from std_msgs.msg import String
import time

def capture_image(camera):
    stream = BytesIO()
    camera.capture(stream, 'jpeg')
    stream.seek(0)
    image_pil = pilimage.open(stream)
    return image_pil
    

def imager():
    pub = rospy.Publisher('pi', String, queue_size=10)
    rospy.init_node('pi', anonymous=True)
    # unsure of camera capture rate - need to check, but pertty sure it's slow atm
    rate = rospy.Rate(1) # Hz

    while not rospy.is_shutdown():

        rospy.loginfo('Generate string')
        # img = capture_image(picam)
        # img = np.array(img)

        # br = CvBridge()
        # pub.publish(br.cv2_to_imgmsg(img))
        pub.publish("Hello from PiLand")
        
        rate.sleep()


if __name__ == '__main__':
    try:
        imager()
    except rospy.ROSInterruptException:
        pass

