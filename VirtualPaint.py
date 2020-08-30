import numpy as np
import cv2 as cv

framewidth = 640
frameheight = 480

cap = cv.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)
cap.set(10,150)

mycolors = [[5,107,0,19,255,255],[133,56,0,159,156,255],[57,76,0,100,255,255]]
mycolorvalues = [[51,153,255], [255,0,255], [0,255,0]]
mypoints = []

def findColor(img,mycolors,mycolorvalues):
    imghsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in mycolors:   
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(imghsv,lower,upper)
        x,y = getContours(mask)
        cv.circle(imgResult,(x,y),10,mycolorvalues[count],cv.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])        
        count += 1
        # cv.imshow(str(color[0]), mask)
    return newpoints

def getContours(img):
    contours, hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area>500:
            # cv.drawContours(imgResult, cnt,-1, (255,0,0), 3)
            peri = cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt, 0.02*peri,True)
            x,y,w,h = cv.boundingRect(approx)
    return x+w//2,y

def drawoncanvas(mypoints, mycolorvalues):
    for point in mypoints:
        cv.circle(imgResult,(point[0],point[1]),10,mycolorvalues[point[2]],cv.FILLED)

while True:
    success, img = cap.read() 
    img = cv.flip(img,1)
    imgResult = img.copy()
    newpoints = findColor(img,mycolors,mycolorvalues )
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(mypoints)!=0:
        drawoncanvas(mypoints,mycolorvalues)
    cv.imshow('Result',imgResult)
    if cv.waitKey(1) & 0xff == ord('q'):
        break