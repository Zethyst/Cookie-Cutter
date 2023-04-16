import os
import cv2 
import numpy as np
from cvzone import HandTrackingModule, overlayPNG

folderPath = 'frames'
mylist = os.listdir(folderPath)
graphic = [cv2.imread(f'{folderPath}/{imPath}') for imPath in mylist]
intro = graphic[0];
kill =graphic[1];
winner = graphic[2];
cam = cv2.VideoCapture(0)
detector = HandTrackingModule.HandDetector(maxHands=1,detectionCon=0.77)
# sets the minimum confidence threshold for the detection

#INITILIZING GAME COMPONENTS
#----------------------------------------------------------------

sqr_img = cv2.imread("img\sqr(2).png", cv2.IMREAD_UNCHANGED)
mlsa = cv2.imread("img\mlsa.png", cv2.IMREAD_UNCHANGED)
sqr_img = cv2.resize(sqr_img, (270, 230), interpolation=cv2.INTER_AREA)
mlsa = cv2.resize(mlsa, (90, 80), interpolation=cv2.INTER_AREA)

cordinatex, cordinatey = 160,160
b,g,r = 27,74,114 

px,py =0,0
fx,fy =0,0

NotWon = True
gameOver = False
again=False
smoothX ,smoothY = 0,0

canvas = np.zeros((480,640,3),np.uint8)

smoothing = 2
corners = [0,0,0,0] 
errorcount =0 

#INTRO SCREEN WILL STAY UNTIL Q IS PRESSED

while True:
    cv2.imshow('Squid Game', cv2.resize(intro, (640,480), interpolation=cv2.INTER_AREA))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# gameOver = False
# NotWon =True

while not gameOver:
    _, img = cam.read()
    img = cv2.flip(img,1)
    hands,img = detector.findHands(img, flipType = False) 
    time =0 
    h,w,_ = sqr_img.shape
    img = overlayPNG(img,sqr_img,[cordinatex,cordinatey])#placeing the cookie image
    img = overlayPNG(img,mlsa,[0,0]) #placing the mlsa image
    if hands:
        lmList = hands[0]['lmList'] 
        cursor = lmList[8]
        smoothX = int(px + (cursor[0] - px) / smoothing)
        smoothY = int(py + (cursor[1] - py) / smoothing)
        if detector.fingersUp(hands[0]) == [0,1,0,0,0]: 
            if cordinatex < smoothX < cordinatex + w and cordinatey < smoothY < cordinatey + h:
                colorblue, colorgreen, colorred = img[smoothY, smoothX, 0], img[smoothY, smoothX, 1], img[smoothY, smoothX, 2]
                if colorblue == b and colorgreen == g and colorred == r:
                    time=time +1
                    if px!=cursor[0] and py!=cursor[1]:
                        if px == 0 and py == 0:
                            px, py = cursor[0], cursor[1]
                        if fx == 0 and fy == 0:
                            fx, fy = cursor[0], cursor[1] #set he end point
                        cv2.line(canvas,(px, py),(smoothX,smoothY),(0,0,255),thickness=9)
                        if(smoothX-10 <= fx <= smoothX + 10 and smoothY-10 <= fy <= smoothY):
                            if corners == [1,1,1,1]:
                                print("YOU WON!!")
                                NotWon = False 
                                gameOver =True

                                if gameOver:
                                     for i in range(10):
                                        cv2.imshow('Squid Game', cv2.resize(winner, (0, 0), fx=0.69, fy=0.69))
                                     while True:
                                       cv2.imshow('Squid Game', cv2.resize(winner, (0, 0), fx=0.49, fy=0.49))
                                       if cv2.waitKey(10) & 0xFF == ord('q'):
                                           break
                                       if cv2.waitKey(10) & 0xFF == ord('p'):
                                         print("Playing again!")
                                         again=True
                                         break
                        if again:
                            continue
                elif colorblue == b and colorgreen == g and colorred == 26:
                    corners[0] = 1
                    cv2.line(canvas, (px, py), (smoothX, smoothY), (0,0,255), thickness=9)
                elif colorblue == b and colorgreen == g and colorred == 28: 
                    corners[1] = 1
                    cv2.line(canvas, (px, py), (smoothX, smoothY), (0,0,255), thickness=9)
                elif colorblue == b and colorgreen == g and colorred == 29:
                    corners[2] = 1
                    cv2.line(canvas, (px, py), (smoothX, smoothY), (0,0,255), thickness=9)
                elif colorblue == b and colorgreen == g and colorred == 30:
                    corners[3] = 1
                    cv2.line(canvas, (px, py), (smoothX, smoothY), (0,0,255), thickness=9)
                else:
                    errorcount += 1
                    if errorcount == 40 or time == 1:
                        print("You LOSE!")
                        gameOver = True
                        errorcount = 0
                        corners = [0, 0, 0, 0]
                        canvas = np.zeros((480, 640, 3), np.uint8) 
                        fx, fy = 0, 0
                        px, py = 0, 0
                        c = 0
                cv2.circle(img, (smoothX, smoothY), 5, (0,0,255), cv2.FILLED)
        else:
            px, py = 0, 0
            cv2.circle(img, (smoothX, smoothY), 5, (0,0,255), cv2.FILLED)
        px, py = smoothX, smoothY

    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, canvas)

    cv2.imshow('Squid Game', cv2.resize(img, (0, 0), fx=0.79, fy=0.79))
    cv2.waitKey(3)

#LOSS SCREEN
if NotWon:
    for i in range(10):
       cv2.imshow('Squid Game', cv2.resize(kill, (0, 0), fx=0.69, fy=0.69))
    while True:
        cv2.imshow('Squid Game', cv2.resize(kill, (0, 0), fx=0.49, fy=0.49))
        if cv2.waitKey(1) & 0xFF == ord('q'):
         break
        if cv2.waitKey(1) & 0xFF == ord('p'):
         print("Playing again!")

else:
    #WIN SCREEN
    cv2.imshow('Squid Game', cv2.resize(winner, (0, 0), fx=0.49, fy=0.49))
    cv2.waitKey(1)

    while True:
     cv2.imshow('Squid Game', cv2.resize(winner, (0, 0), fx=0.49, fy=0.49))
     if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
