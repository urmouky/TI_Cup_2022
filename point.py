import numpy as np
import cv2

"This File is shit"

cap = cv2.VideoCapture(1)
while(1):
    flag, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,25,0.04)
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    # Threshold for an optimal value, it may vary depending on the image.
    frame[dst>0.01*dst.max()]=[0,0,255]
    cv2.imshow('dst',frame)
    if cv2.waitKey(1) & 0xff == 27:
        break


cv2.destroyAllWindows()
