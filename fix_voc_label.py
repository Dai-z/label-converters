import xml.etree.ElementTree as ET
import os
from os import listdir, getcwd
from os.path import join
import argparse


# classes = [
#     "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
#     "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
#     "pottedplant", "sheep", "sofa", "train", "tvmonitor"
# ]
classes = []


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def parse_cls(anno_files, args):
    for anno in anno_files:
        if not '.xml' in anno:
            continue
        anno_file = join(args.anno_dir, anno)

        if not os.path.isfile(anno_file):
            continue
        in_file = open(anno_file)

        tree = ET.parse(in_file)
        root = tree.getroot()

        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                classes.append(cls)

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

    have_obj = False
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name')
        if cls.text == args.src_label:
            print('Fixed '+cls.text)
            cls.text = args.dst_label
        have_obj = True
    tree.write(anno_file)

    return have_obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--anno_dir",
                        help="Directory for VOC annotation xml files")
    parser.add_argument("--src_label",
                        help="Label need to be fixed")
    parser.add_argument("--dst_label",
                        help="New label name")
    args = parser.parse_args()

    anno_files = listdir(args.anno_dir)

    for anno in anno_files:
        res = convert_annotation(anno, args)
