import argparse
from lxml import etree, objectify
import os
import cv2
from os.path import join

parse = argparse.ArgumentParser()

parse.add_argument('--class_list',
                   type=str,
                   default='classes.txt',
                   help='get class name from class_list file')
parse.add_argument('--label_dir',
                   type=str,
                   required=True,
                   help='convert yolo labels(txt file) in label_dir')
args = parse.parse_args()

label_path = os.path.abspath(args.label_dir)
if os.path.isfile(args.class_list):
    list_file = args.class_list
else:
    list_file = join(label_path, args.class_list)

class_list = []
with open(list_file) as f:
    for line in f:
        class_list.append(line.strip())
if not os.path.isdir(label_path.replace('labels', 'annotations')):
    os.mkdir(label_path.replace('labels', 'annotations'))

label_files = os.listdir(label_path)
for label_file in label_files:
    if label_file == args.class_list:
        continue
    label_file = join(args.label_dir, label_file)
    if label_file == args.class_list:
        continue
    image_file = label_file.replace('.txt', '.jpg').replace('labels', 'images')
    voc_file = label_file.replace('.txt',
                                  '.xml').replace('labels', 'annotations')
    if not os.path.isfile(image_file):
        print("Image {} doesn't exist!".format(image_file))
        continue
    img = cv2.imread(image_file)
    shape = img.shape
    with open(label_file) as f:
        print('Processing {}'.format(label_file))
        E = objectify.ElementMaker(annotate=False)
        # xml head
        anno_tree = E.annotation(
            E.filename(image_file.split('/')[-1]),
            E.size(E.width(shape[0]), E.height(shape[1]), E.depth(shape[2])),
            E.segmented(0))
        for line in f:
            [c, x, y, w, h] = line.split(' ')
            name = class_list[int(c)]
            x = float(x) * shape[1]
            y = float(y) * shape[0]
            w = float(w) * shape[1]
            h = float(h) * shape[0]
            xmin = x - w / 2
            ymin = y - h / 2
            xmax = x + w / 2
            ymax = y + h / 2
            obj = E.object(
                E.name(name),
                E.bndbox(E.xmin(int(xmin)), E.ymin(int(ymin)),
                         E.xmax(int(xmax)), E.ymax(int(ymax))), E.difficult(0))
            anno_tree.append(obj)
        etree.ElementTree(anno_tree).write(voc_file, pretty_print=True)
