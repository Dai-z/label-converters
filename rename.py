import os
from os.path import join
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--image_dir',
                    dest='image_dir',
                    type=str,
                    required=True,
                    help='generae list of all images in the dir')

args = parser.parse_args()

image_dir = os.path.abspath(args.image_dir)
image_list = os.listdir(args.image_dir)
txt_dir = image_dir.replace('JPEGImages', 'labels').replace('images','labels')
xml_dir = image_dir.replace('JPEGImages', 'annotations').replace('images','annotations')
if not os.path.isdir(xml_dir):
    xml_dir.replace('annotations', 'Annotations')
if not os.path.isdir(xml_dir):
    xml_dir = None
if not os.path.isdir(txt_dir):
    txt_dir = None

cnt = 0
image_list.sort()
for img in image_list:
    print('Renaming: '+os.path.join(image_dir, img))
    prefix = img.rsplit('.')[0]
    new = 'image_{0:05}'.format(cnt)
    # Rename image
    src = os.path.join(image_dir, img)
    dst = os.path.join(image_dir, new+'.'+img.split('.')[-1])
    os.rename(src, dst)
    # Rename txt
    if txt_dir:
        src = os.path.join(txt_dir, prefix+'.txt')
        dst = os.path.join(txt_dir, new+'.txt')
        if os.path.isfile(src):
            print('Renaming: '+src)
            os.rename(src, dst)
    # Rename xml
    if xml_dir:
        src = os.path.join(xml_dir, prefix+'.xml')
        dst = os.path.join(xml_dir, new+'.xml')
        if os.path.isfile(src):
            print('Renaming: '+src)
            os.rename(src, dst)
    cnt+=1

