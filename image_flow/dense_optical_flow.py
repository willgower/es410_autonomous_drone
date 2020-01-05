import cv2
import numpy as np
cap = cv2.VideoCapture(0)

ret, old_frame = cap.read()
prvs = cv2.cvtColor(old_frame,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(old_frame)
hsv[...,1] = 255

while(1):
    ret, new_frame = cap.read()
    next = cv2.cvtColor(new_frame,cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('new frame',rgb)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png',new_frame)
        cv2.imwrite('opticalhsv.png',rgb)
    prvs = next

cap.release()
cv2.destroyAllWindows()
