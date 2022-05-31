import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)

#帧640*480;亮度100/256
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
cap.set(cv2.CAP_PROP_BRIGHTNESS,100)

myColors = [[0,0,185,15,15,255],
    [120,10,180,170,40,255]]              
            #绿色[35,15,180,77,40,255]
            #颜色列表 h_low,s_low,v_low,h_high,s_high,v_high
#myColors = [[0,0,200,255,255,255]]

def findColor(frame,myColors):
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for color in myColors:
        lower = np.array(color[0:3])    #下限
        upper = np.array(color[3:6])    #上限
        mask = cv2.inRange(imgHSV,lower,upper)

        contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)     #查找轮廓
    
        rect_x,rect_y,rect_w,rect_h = 0,0,0,0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>10:
                cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
                peri = cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)
                rect_x,rect_y,rect_w,rect_h = cv2.boundingRect(approx)

        cv2.circle(imgResult,(rect_x+rect_w//2,rect_y+rect_h//2),5,(0,255,0),cv2.FILLED)
        cv2.imshow("str(color[i])",mask)


while True:
    flag, frame = cap.read()
    imgResult = frame.copy()
    findColor(frame,myColors)
    cv2.imshow("video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break