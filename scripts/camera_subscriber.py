# /usr/bin/env python3


"""
project: coral_spawn_imager 
file: camera subscriber
A ROS node that subscribes to the camera image topic and replays/saves the image
author: Dorian Tsai
email: dorian.tsai@gmail.com
date: 2022/Oct/07
"""


import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 as cv


class ImageReceiver(object):
    def __init__(self):
        # params
        self.image = None
        self.br = CvBridge()
        self.loop_rate = rospy.Rate(1) # Hz
        cv.namedWindow("picam image", cv.WINDOW_NORMAL)
        cv.resizeWindow("picam image", 648, 486)

        # subscriber:
        rospy.Subscriber('/image', Image, self.callback)

    def callback(self, msg):
        rospy.loginfo('Image received...')
        self.image = self.br.imgmsg_to_cv2(msg)

        # show the image
        cv.imshow("picam image", receiver.image)
        cv.waitKey(2)


if __name__ == '__main__':
    try:
        rospy.init_node('receiver', anonymous=True)
        receiver = ImageReceiver()
        rospy.spin()
        cv.destroyAllWindows()

    except rospy.ROSInterruptException:
        pass
