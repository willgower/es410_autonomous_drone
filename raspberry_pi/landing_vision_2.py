# ES410 Autonomous Drone
# Owner: William Gower
# File: landing_vision_2.py
# Description: Module to process images and return high level movement commands

import cv2
import numpy as np
import socket
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

        self.max_features = 100
        self.good_match_percent = 0.1

        if socket.gethostname() != "william-XPS-13-9360":
            self.camera = PiCamera()

    def take_picture(self):
        raw_capture = PiRGBArray(self.camera)
        time.sleep(0.1)
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

        # Detect ORB features and compute descriptors.
        orb = cv2.ORB_create(self.max_features)
        keypoints1, descriptors1 = orb.detectAndCompute(ground_grey, None)
        keypoints2, descriptors2 = orb.detectAndCompute(self.landing_logo_grey, None)

        # Match features.
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(descriptors1, descriptors2, None)

        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)

        # Remove not so good matches
        num_good_matches = int(len(matches) * self.good_match_percent)
        matches = matches[:num_good_matches]

        # Extract location of good matches
        points1 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt

        average = points1.mean(0, int)

        if test is not None:
            mid = cv2.circle(ground, (average[0], average[1]), 50, (255, 0, 0), -1)
            cv2.line(mid, (0, int(ground.shape[0] / 2)), (ground.shape[1], int(ground.shape[0] / 2)), (255, 255, 255), 10)
            cv2.line(mid, (int(ground.shape[1] / 2), 0), (int(ground.shape[1] / 2), ground.shape[0]), (255, 255, 255), 10)
            cv2.imwrite("images/located_" + test + ".jpg", mid)

        coords = [int(average[0] - ground.shape[1] / 2), int(ground.shape[0] / 2 - average[1])]

        x_distance = round((coords[0] / 1296) * altitide * 0.51, 2)
        y_distance = round((coords[1] / 972) * altitide * 0.37, 2)

        return x_distance, y_distance


if __name__ == '__main__':
    vision = LandingVision()

    for i in "1", "2", "3", "4":
        # Ground image to search within
        ground = cv2.imread("images/large_image_" + i + ".jpeg", cv2.IMREAD_COLOR)

        offset = vision.get_offset(20, ground, test=i)
        print(offset)
