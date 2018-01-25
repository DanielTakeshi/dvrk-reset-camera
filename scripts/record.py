import cv2, os, pickle, sys, tfx, time
import numpy as np
from dvrk.robot import robot
from autolab.data_collector import DataCollector


if __name__ == "__main__":
    d = DataCollector()
    r1 = robot("PSM1") # left (but my right)
    r2 = robot("PSM2") # right (but my left)
    time.sleep(2)

    #cv2.imshow("left image, press any key", d.left_image)
    #key = cv2.waitKey(0)
    #cv2.imshow("right image, press any key", d.right_image)
    #key = cv2.waitKey(0)

    cv2.imshow("left image with boxes, press any key", d.left_bbox)
    key = cv2.waitKey(0)
    cv2.imshow("right image with boxes, press any key", d.right_bbox)
    key = cv2.waitKey(0)

    cv2.imwrite('images/left_raw.png',   d.left_image)
    cv2.imwrite('images/left_bbox.png',  d.left_bbox)
    cv2.imwrite('images/right_raw.png',  d.right_image)
    cv2.imwrite('images/right_bbox.png', d.right_bbox)

