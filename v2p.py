import os
import cv2
import numpy as np

cap = cv2.VideoCapture('/home/daiz/Videos/record.avi')
cnt = 0
_, image = cap.read()
skip_num = 60

def show_skip(image, scale):
    global skip_num
    tmp = image
    tmp	= cv2.putText(tmp, str(skip_num), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, int(3*scale),(0,0,255), int(6*scale))
    cv2.imshow('current', tmp)
    key = cv2.waitKey(5)
    if key == 119: # w
        skip_num += 5
    elif key == 115: # s
        skip_num -= 5
        if skip_num < 0:
            skip_num = 0
    elif key == 114: # r
        skip_num = 60
        return 1
    return 0

cv2.namedWindow('current', 0)
while len(image) > 0:
    f_name = '/home/daiz/Data/tmp/JPEGImages/tmp_'+str(cnt)+'.jpg'
    _, image = cap.read()
    cv2.imwrite(f_name, image)
    scale = image.shape[0]/1080
    show_skip(image, scale)
    for i in range(skip_num):
        _, image = cap.read()
        ret = show_skip(image, scale)
        if ret:
            break

    image = image.astype(np.uint8)
    cnt+=1
    print(f_name)
