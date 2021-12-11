import cv2 as cv
import numpy as np
import time
import HandTrackingModule as htm
import autopy

#########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 5
###########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0


cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    # 1. Find hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        cv.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255,0,255),2)

        # 4. Only Index Finger: Moving mode
        if fingers[1]==1:# and fingers[2]==0:

            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR,wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR), (0,hScr))

            # 6. Smooth Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. Move Mouse
            autopy.mouse.move(wScr-clocX, clocY)
            cv.circle(img, (x1,y1), 15, (255,0,255), cv.FILLED)
            plocX, plocY = clocX, clocY
        ### Clicking thumb: left click
        if fingers[2]==0 and fingers[3]  ==  1:
            autopy.mouse.click() #toggle(autopy.mouse.Button.LEFT, True)
        #else:
        #    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
        #### Clicking middle finger: right click
        if fingers[3] == 0 and fingers[2] == 1:
            autopy.mouse.click(autopy.mouse.Button.RIGHT) #toggle(autopy.mouse.Button.RIGHT, True)
        #else:
        #    autopy.mouse.toggle(autopy.mouse.Button.RIGHT, False)
        #if fingers[0] == 0 and fingers[2] == 0:
        #    autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, True)
        #else:
        #    autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, False)
        
    # 8. Both Index and middle fingers are up: Clicking mode
    #if fingers[1] == 1 and fingers[2] == 1:
        #length, img, _ = detector.findDistance(8, 12, img)
        #print(length)
    # 9. Find distance between fingers
    # 10. Click mouse if distance short
    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (20,50), cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    # 12. Display
    cv.imshow("image", img)
    cv.waitKey(1)