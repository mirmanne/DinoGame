# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:57:42 2022

@author: mirma
"""
import cv2
import mediapipe as mp
import pyautogui 
import time

class handDetector():
    def __init__(self, mpHands, hands, mpDraw):
        self.mpHands = mp.solutions.hands
        self.hands = hands
        self.mpDraw = mpDraw
        
    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
        return lmlist

def click(key):
   pyautogui.keyDown(key)
   return

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    jump = False
    prevjump = False
    hands = mpHands.Hands(static_image_mode=False,  
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    detector = handDetector(mpHands, hands, mpDraw)

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist) != 0:
            print('thumb')
            print(lmlist[4])
            print('finger')
            print(lmlist[8])
            tid, tx, ty = lmlist[4]
            pid, px, py = lmlist[8]
            if ty - py >= 50:
                jump = True
            else:
                jump = False
            if prevjump != jump:
                prevjump = jump
                if jump == True:
                    click("up")         

            

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        if jump:
            cv2.putText(img, 'JUMP', (100, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release() 
    cv2.destroyAllWindows()


if __name__ == "__main__":
    time.sleep(5)
    main()
