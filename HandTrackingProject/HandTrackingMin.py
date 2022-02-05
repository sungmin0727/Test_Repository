from cv2 import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Frame rate 구하기 위함
# previous time, currenct time
pTime = 0
cTime = 0

while True :
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    lmList = []

    if results.multi_hand_landmarks :
        for handLms in results.multi_hand_landmarks :
            for id, lm in enumerate(handLms.landmark) :
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y*h)

                # 엄지
                if id == 4  :
                    cv2.circle(img, (cx,cy), 10, (0,255,255), cv2.FILLED)
                    print(id, cx, cy)
                    lmList.append(cx)
                    lmList.append(cy)
                # 검지
                if id == 8:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)
                    print(id, cx, cy)
                    lmList.append(cx)
                    lmList.append(cy)

            # 위에서 엄지와 검지가 검출이 되었다면, lmList에 4개의 값(엄지 cx,cy \ 검지 cx,cy) 존재
            # 따라서 if len(lmList) == 4 :
            if len(lmList) == 4 :
                    print(lmList)
                    x1, y1 = lmList[0], lmList[1]
                    x2, y2 = lmList[2], lmList[3]
                    cv2.line(img, (x1,y1), (x2,y2), (255,0,255),3)
                    cv2.circle(img, ((x2+x1)//2, (y2+y1)//2), 5, (255, 0, 0), cv2.FILLED)


            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS,
                                  mp_drawing_styles.DrawingSpec(color=(0,0,255)),
                                  mp_drawing_styles.DrawingSpec(color=(0,255,0)))

            lmList.clear()




    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
