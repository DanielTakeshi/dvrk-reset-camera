import numpy as np
import rospy
from geometry_msgs.msg import PointStamped, Point
from visualization_msgs.msg import Marker
import cv2
import cv_bridge
import numpy as np
import scipy.misc
import pickle
import imutils
import time
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from config.constants import *
import string
import random
"""
The DataCollector class polls data from the rostopics periodically. It manages 
the messages that come from ros.
"""

class DataCollector:

    def __init__(self, 
                 camera_left_topic="/endoscope/left/",
                 camera_right_topic="/endoscope/right/",
                 camera_info_str='camera_info',
                 camera_im_str='image_rect_color'):

        self.right_image = None
        self.left_image = None

        # Bounding box of left image's points. MUST EXPERIMENT WITH THIS.
        self.lx, self.ly = 710, 160 
        self.lw, self.lh = 725, 645
        # Right image. EXPERIMENT.
        self.rx, self.ry = 625, 160
        self.rw, self.rh = 725, 645

        self.info = {'l': None, 'r': None}
        self.bridge = cv_bridge.CvBridge()
        self.timestep = 0
        self.identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

        rospy.Subscriber(camera_left_topic + camera_im_str, Image,
                         self.left_image_callback, queue_size=1)
        rospy.Subscriber(camera_right_topic + camera_im_str, Image,
                         self.right_image_callback, queue_size=1)
        rospy.Subscriber(camera_left_topic + camera_info_str,
                         CameraInfo, self.left_info_callback)
        rospy.Subscriber(camera_right_topic + camera_info_str,
                         CameraInfo, self.right_info_callback)

    def left_info_callback(self, msg):
        if self.info['l']:
            return
        self.info['l'] = msg

    def right_info_callback(self, msg):
        if self.info['r']:
            return
        self.info['r'] = msg

    def right_image_callback(self, msg):
        if rospy.is_shutdown():
            return
        x,y,w,h = self.rx, self.ry, self.rw, self.rh
        self.right_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        self.right_bbox = self.make_bounding_box(self.right_image, x,y,w,h)

    def left_image_callback(self, msg):
        if rospy.is_shutdown():
            return
        x,y,w,h = self.lx, self.ly, self.lw, self.lh
        self.left_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        self.left_bbox = self.make_bounding_box(self.left_image, x,y,w,h)

    def make_bounding_box(self, img, x,y,w,h):
        """ Make a bounding box with labels. """
        img = img.copy()
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,0), 2)
        cv2.circle(img=img,
                   center=(x,y),
                   radius=5, 
                   color=(0,0,255), 
                   thickness=-1)
        cv2.circle(img=img,
                   center=(x+w,y+h),
                   radius=5, 
                   color=(0,0,255), 
                   thickness=-1)
        cv2.putText(img=img,
                    text="{}".format((x,y)),
                    org=(x,y),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale=1, 
                    color=(0,255,0), 
                    thickness=2)
        cv2.putText(img=img,
                    text="{}".format((x+w,y+h)),
                    org=(x+w,y+h),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale=1, 
                    color=(0,255,0), 
                    thickness=2)
        return img
