# ES410 Autonomous Drone
# Owner: Aaron Sodhi
# File: landing_vision.py
# Description: Module to process images and return high level movement commands

# Return a tuple of form (x, y, yaw_angle)

# =============== NOTES ===============
# → bare bones completed by JRB so DroneControl can be written
# → Aaron, you need to specify what input arguments you want to
#   the get_instruction() method
# → Formatting and edit for use on RPi by Will
# =====================================

import io
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from collections import deque
import imutils
import cv2


class LandingVision:
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def sift_detector(self, new_image, image_template):
        # Function that compares input image to template
        # It then returns the number of SIFT matches between them
        image1 = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
        image2 = image_template

        # Create SIFT detector object
        sift = cv2.xfeatures2d.SIFT_create()

        # Obtain the keypoints and descriptors using SIFT
        keypoints_1, descriptors_1 = sift.detectAndCompute(image1, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(image2, None)

        # Define parameters for our Flann Matcher
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=3)
        search_params = dict(checks=100)

        # Create the Flann Matcher object
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # Obtain matches using K-Nearest Neighbor Method
        # the result 'matchs' is the number of similar matches found in both images
        matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)

        # Store good matches using Lowe's ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        return len(good_matches)

    def get_instruction(self, altitude):
        while altitude > 
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        cap = PiRGBArray(camera, size=(640, 480))
        
        # allow the camera to warmup
        time.sleep(0.1)

        # Load our image template, this is our reference image - the drone logo
        image_template = cv2.imread('DroneLogo.png',0) 

        while True:
            # Get webcam images
            ret, frame = cap.read()

            # Get height and width of webcam frame
            height, width = frame.shape[:2]

            # Define ROI Box Dimensions
            #top_left_x = int (width / 3)
            #top_left_y = int ((height / 2) + (height / 4))
            #bottom_right_x = int ((width / 3) * 2)
            #bottom_right_y = int ((height / 2) - (height / 4))
            top_left_x = width
            top_left_y = height
            bottom_right_x = 0
            bottom_right_y = 0

            # Draw rectangular window for our region of interest   
            window = cv2.rectangle(frame, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), 255, 0)

            # Get number of SIFT matches
            matches = sift_detector(window, image_template)

            # Display status string showing the current no. of matches 
            cv2.putText(frame,str(matches),(450,450), cv2.FONT_HERSHEY_COMPLEX, 2,(0,255,0),1)

            # Our threshold to indicate object deteciton
            # We use 10 since the SIFT detector returns little false positves
            threshold = 90

            # If matches exceed our threshold then logo has been detected
            if matches > threshold:

                # define the lower and upper boundaries of the "red object"
                # (or "ball") in the HSV color space, then initialize the
                # list of tracked points
                colorLower = (0, 100, 100)
                colorUpper = (180, 255, 255)
                pts = deque()

                # resize the frame, inverted ("vertical flip" w/ 180degrees),
                # blur it, and convert it to the HSV color space
                frame = imutils.resize(frame, width=600)
                # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # construct a mask for the color "red", then perform
                # a series of dilations and erosions to remove any small
                # blobs left in the mask
                mask = cv2.inRange(hsv, colorLower, colorUpper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                # find contours in the mask and initialize the current
                # (x, y) center of the ball
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None

                # only proceed if at least one contour was found
                if len(cnts) > 0:
                    # find the largest contour in the mask, then use
                    # it to compute the minimum enclosing circle and
                    # centroid
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    # only proceed if the radius meets a minimum size
                    if radius > 10:
                            # draw the circle and centroid on the frame,
                            # then update the list of tracked points
                            cv2.circle(frame, (int(x), int(y)), int(radius),
                                    (0, 255, 255), 2)
                            cv2.circle(frame, center, 5, (0, 0, 255), -1)

                # update the points queue
                pts.appendleft(center)

                #calculate the x,y coordinates from the centre of field of view to centre of logo
                x_logo = center[0]
                y_logo = center[1]
                x_coordinate = (width/2) - x_logo
                y_coordinate = (height/2) - y_logo
                logo_coordinates = [x_coordinate, y_coordinate]
                
                #determine pixel and actual dimensions
                
                
                #initiate landing when drone is centered on landing zone logo
                while logo_coordinates == [0, 0]:
                    altitude -= 0.5

                # loop over the set of tracked points
                for i in range(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                    if pts[i - 1] is None or pts[i] is None:
                            continue
            # capture frames from the camera
            for frame in camera.capture_continuous(cap, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                image = frame.array
                # show the frame
                cv2.imshow("Frame", image)
                key = cv2.waitKey(1) & 0xFF
                # clear the stream in preparation for the next frame
                cap.truncate(0)
                # if the `q` key was pressed, break from the loop
                if key == ord("q"):

        cap.release()
        cv2.destroyAllWindows()

        return x_vel, y_vel, yaw_vel
