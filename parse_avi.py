import numpy as np
import cv2
import os

cap = cv2.VideoCapture('camera_2_small.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter('output0.avi', fourcc, 30.0, (1280,720))
nr = 0
nr2 = 0
idx = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret!=True:
        break
    fisn = "Output/frame" + str(nr2) + ".jpg"
    cv2.imwrite(fisn,frame)
    nr2 = nr2+1
   
    if nr2 % 10 !=0:
        continue
    nr = nr + 1
    print (nr2)
    if nr<60*30:
    	out.write(frame)
    else:
        out.write(frame)
        idx+=1
        nr = 0
        name = "output" + str(idx) + ".avi"
        out.release()
        out = cv2.VideoWriter(name,fourcc, 30.0, (1280,720))	

print(nr)
cap.release()

