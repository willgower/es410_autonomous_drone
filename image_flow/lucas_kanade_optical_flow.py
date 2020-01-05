import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#Corner detection
feature_variables = dict(maxCorners = 100, qualityLevel = 0.3, minDistance = 7, blockSize = 7 )

#Lucas-Kanade variables set
l_k_variables = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

#Assign colours using random function
colours = np.random.randint(0,255,(100,3))

#Corner detection of first frame
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_variables)

#Creating mask for the image
mask = np.zeros_like(old_frame)

while(1):
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Optical flow calculation
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **l_k_variables)

    #Select ideal points in the frame
    point_new = p1[st==1]
    point_prev = p0[st==1]

    #Draw lines to track optical flow
    for i,(new,old) in enumerate(zip(point_new,point_prev)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), colours[i].tolist(), 2)
        frame = cv2.circle(frame,(a,b),5,colours[i].tolist(),-1)
    image = cv2.add(frame,mask)

    cv2.imshow('frame',image)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = point_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()
