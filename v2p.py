import os
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--video',
                    dest='video',
                    type=str,
                    required=True,
                    help='Input video')
parser.add_argument('--image_dir',
                    dest='image_dir',
                    type=str,
                    required=True,
                    help='image saving dir')

args = parser.parse_args()

cap = cv2.VideoCapture(args.video)
prefix=args.image_dir.strip('/').split('/')[-1] + '_'

cnt = -1
tmp_list=os.listdir(args.image_dir)
tmp_list.sort()
image_list = []
for img in tmp_list:
    if prefix in img:
        num = int(img.split('.')[0].split('_')[-1])
        if num > cnt:
            cnt = num
    else:
        image_list.append(img)
cnt += 1
_, image = cap.read()
skip_num = 60

def show_skip(image, scale, wait=5):
    global skip_num
    tmp = image
    tmp	= cv2.putText(tmp, str(skip_num), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, int(3*scale),(0,0,255), int(6*scale))
    cv2.imshow('current', tmp)
    key = cv2.waitKey(wait)
    if key == 119: # w
        skip_num += 5
    elif key == 115: # s
        skip_num -= 5
    elif key == 97: # a
        skip_num -= 1000
    elif key == 100: # d
        skip_num += 1000
    elif key == 114: # r
        skip_num = 60
        return 1
    elif key == 32: # space for pause
        print('Paused')
        while (cv2.waitKey(0) != 32):
            pass
        print('Continue')
    if skip_num < 0:
        skip_num = 0
    return 0

cv2.namedWindow('current', 0)
while len(image) > 0:
    f_name = os.path.join(args.image_dir, prefix+'{0:05}'.format(cnt)+'.jpg')
    _, image = cap.read()
    cv2.imwrite(f_name, image)
    scale = image.shape[0]/1080
    show_skip(image, scale)
    for i in range(skip_num):
        _, image = cap.read()
        if cnt > 1000:
            _, image = cap.read()
        for i in range(cnt//5000):
            _, image = cap.read()
        ret = show_skip(image, scale,1)
        if ret:
            break

    image = image.astype(np.uint8)
    cnt+=1
    print(f_name)
