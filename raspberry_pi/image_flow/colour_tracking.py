'''Inspiration from OpenCV-Python Tutorials
Taken from Changing Colorspaces
Link at:
https://opencv-python-tutroals.readthedocs.io
/en/latest/py_tutorials/py_imgproc/py_colorspaces
/py_colorspaces.html#converting-colorspaces'''


import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Capture each frame
    _, capture = cap.read()

    #BGR to HSV conversion
    hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)

    # Set range for HSV blue color
    blue_start = np.array([110,50,50])
    blue_end = np.array([130,255,255])

    # Restrict HSV image to track blue colors only
    mask = cv2.inRange(hsv, blue_start, blue_end)

    # Bitwise-AND mask and original image
    tracked_image = cv2.bitwise_and(capture,capture, mask= mask)

    cv2.imshow('capture frame',capture)
    cv2.imshow('mask',mask)
    cv2.imshow('tracked image',tracked_image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
