import os
import cv2
import numpy as np

cap = cv2.VideoCapture('/home/daiz/Videos/record.avi')
cnt = 0
_, image = cap.read()
while len(image) > 0:
    f_name = '/home/daiz/Data/tmp/JPEGImages/tmp_'+str(cnt)+'.jpg'
    cv2.imwrite(f_name, image)
    _, image = cap.read()
    for i in range(60):
        _, image = cap.read()
    image = image.astype(np.uint8)
    cnt+=1
    print(f_name)
