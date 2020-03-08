# ES410 Autonomous Drone
# Owner: William Gower
# File: landing_vision_2.py
# Description: Module to process images and return high level movement commands

import cv2
import numpy as np
import socket
# Only the Raspberry Pi can take pictures
# Any other computer can still run the testbench
if socket.gethostname() != "william-XPS-13-9360":
    from picamera.array import PiRGBArray
    from picamera import PiCamera
import time


class LandingVision:
    def __init__(self):
        """
        Initialise camera and class attributes
        """
        # Landing image to search for
        self.landing_logo = cv2.imread("images/landing_image.png", cv2.IMREAD_COLOR)
        self.landing_logo_grey = cv2.cvtColor(self.landing_logo, cv2.COLOR_BGR2GRAY)

        # Set up class attributes
        self.max_features = 100
        self.good_match_percent = 0.1
        if socket.gethostname() != "william-XPS-13-9360":
            self.camera = PiCamera()

        # Find the features of the landing zone image
        self.orb = cv2.ORB_create(self.max_features)
        self.keypoints2, self.descriptors2 = self.orb.detectAndCompute(self.landing_logo_grey, None)

    def take_picture(self):
        """
        Take a picture using the Raspberry Pi camera and return it as an image array
        """
        raw_capture = PiRGBArray(self.camera)
        time.sleep(0.1)  # Wait for 0.1 seconds for the camera to load
        self.camera.capture(raw_capture, format="bgr")
        return raw_capture.array

    def get_offset(self, altitide, ground_in=None, test=None):
        """
        Take the current altitude as input.
        Use this and image recognition to determine the horizontal displacement
        from the centre of the landing zone.
        Return this displacement in cartesian coordinates where 0, 0 represents
        the drone being directly over the target.
        """
        if ground_in is None:
            # Take a picture using the Pi Camera here
            ground_grey = cv2.cvtColor(self.take_picture(), cv2.COLOR_BGR2GRAY)
        else:
            # Convert images to grayscale
            ground_grey = cv2.cvtColor(ground_in, cv2.COLOR_BGR2GRAY)

        # Detect ORB features and compute descriptors
        keypoints1, descriptors1 = self.orb.detectAndCompute(ground_grey, None)

        # Match features
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(descriptors1, self.descriptors2, None)

        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)

        # Remove not so good matches
        num_good_matches = int(len(matches) * self.good_match_percent)
        matches = matches[:num_good_matches]

        # Extract location of good matches
        points1 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt

        if len(points1) < 10:
            print("No matchng image found")
            return 0, 0  # If image can't be seen, descend vertically to get a closer look
        else:
            average = points1.mean(0, int)

        # Don't save any images under normal operation - only when running the testbench
        if test is not None:
            mid = cv2.circle(ground, (average[0], average[1]), 100, (255, 0, 0), 50)
            cv2.line(mid, (0, int(ground.shape[0] / 2)), (ground.shape[1], int(ground.shape[0] / 2)), (255, 255, 255), 10)
            cv2.line(mid, (int(ground.shape[1] / 2), 0), (int(ground.shape[1] / 2), ground.shape[0]), (255, 255, 255), 10)
            cv2.imwrite("images/located_" + test + ".jpg", mid)

        # Normalise the coordinates so that (0, 0) is the centre of the image and position of the drone
        coords = [int(average[0] - ground.shape[1] / 2), int(ground.shape[0] / 2 - average[1])]

        # Convert the pixels into metres
        x_distance = round((coords[0] / 1296) * altitide * 0.51, 2)
        y_distance = round((coords[1] / 972) * altitide * 0.37, 2)

        return x_distance, y_distance


########################################
#           MODULE TESTBENCH           #
########################################

if __name__ == '__main__':
    vision = LandingVision()

    for i in "1", "2", "3", "4", "5", "6", "7", "8", "9":
        # Ground image to search within
        ground = cv2.imread("images/test_image_" + i + ".jpeg", cv2.IMREAD_COLOR)

        offset = vision.get_offset(20, ground, test=i)
        print(offset)
