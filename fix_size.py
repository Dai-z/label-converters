import xml.etree.ElementTree as ET
import os
from os import listdir, getcwd
from os.path import join
import argparse
import cv2

classes = []
def convert_annotation(image, args):
    if args.anno_dir:
        anno_file = join(args.anno_dir, image.split('.')[0]) + '.xml'
    
    if not os.path.isfile(anno_file):
        return False
    in_file = open(anno_file)
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if (w <= 0 or h <= 0):
        print('Fixing: '+anno_file)
        img_file = anno_file.replace('Annotations', 'JPEGImages').replace('annotations', 'JPEGImages').replace('.xml','.jpg')
        img = cv2.imread(img_file)
        h, w, _ = img.shape
        size.find('width').text=str(w)
        size.find('height').text=str(h)

    tree.write(anno_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--anno_dir",
                        required=True,
                        help="Directory for VOC annotation xml files")
    args = parser.parse_args()

    anno_files = listdir(args.anno_dir)
    anno_files.sort()

    for anno in anno_files:
        convert_annotation(anno, args)
