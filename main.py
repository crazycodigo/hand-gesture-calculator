import cv2
import mediapipe as mp
import time


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

webcam = cv2.VideoCapture(0)
x = []
y = []

text = ""
k = [0]*18

key_set =     ["", "1", "12", "123", "1234", "01234", "0", "01", "012", "0123", "04", "4", "34", "014", "14", "0124",     "02", "234"]
text_val =    ["", "1",  "2",   "3",    "4",     "5", "6",  "7",   "8",    "9",  "0", "+", "-",    "*", "/", "Crazy Codigo ", "Exit"]

while True:
    success, img = webcam.read()
    modified_img = cv2.flip(img, 1)
    RGB_img = cv2.cvtColor(modified_img, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_img)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = modified_img.shape
                if id==0:
                    x=[]
                    y=[]
                x.append(int((lm.x)*w))
                y.append(int((1-lm.y)*h))
                if len(y) > 20:
                    id = ""
                    big = [x[3], y[8], y[12], y[16], y[20]]
                    small = [x[4], y[6], y[10], y[14], y[18]]

                    for i in range(len(big)):
                        if big[i] > small[i]:
                            id+=str(i)
                    
                    if id in key_set:
                        k[key_set.index(id)]+=1

                    for i in range(len(k)):
                        if k[i] > 20:
                            if i== 16:
                                print("webcame to exit condition")
                                exit()
                            if i==17:
                                try:
                                    ans=str(eval(text))
                                    text = "= "+ans
                                    for i in range(len(k)):
                                        k[i]=0
                                except:
                                    text = ""
                                    for i in range(len(k)):
                                        k[i]=0
                            else:
                                text+=text_val[i]
                                for i in range(len(k)):
                                    k[i]=0
            
            cv2.putText(modified_img, text, (60,80), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 5)
            mpDraw.draw_landmarks(modified_img, handLms, mpHands.HAND_CONNECTIONS)

    else:
        text = " "
    
    cv2.imshow("Webwebcam", modified_img)
    cv2.waitKey(1)
    
