import xml.etree.ElementTree as ET
import os
from os import listdir, getcwd
from os.path import join
import argparse

sets = [('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'),
        ('2007', 'test')]

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

def parse_cls(img_files, args):
    for image in img_files:
        if args.anno_dir:
            anno_file = join(args.anno_dir, image.split('.')[0]) + '.xml'
        else:
            anno_file = join(args.img_dir, '..', 'Annotations',
                            image.split('.')[0] + '.xml')
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
    else:
        anno_file = join(args.img_dir, '..', 'Annotations',
                         image.split('.')[0] + '.xml')
    if not os.path.isfile(anno_file):
        return False
    in_file = open(anno_file)
    out_file = open(join(args.out_dir, 'labels',
                         image.split('.')[0] + '.txt'), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    have_obj = False
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            print('Error class: '.format(cls))
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(
            str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        have_obj = True
    return have_obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir",
                        help="Output directory for yolo annotation txt files")
    parser.add_argument("--img_dir", help="Directory for images")
    parser.add_argument("--anno_dir",
                        default="",
                        help="Directory for VOC annotation xml files")
    parser.add_argument("--name_file",
                        default="",
                        help="Path to yolo name file")
    parser.add_argument("--list_only",
                        action='store_true',
                        help="Generate for yolo list only.")
    parser.add_argument("--train_set",
                        action='store_true',
                        help="Generate for train set")
    parser.set_defaults(train_set=False)
    parser.set_defaults(list_only=False)
    args = parser.parse_args()

    img_files = listdir(args.img_dir)
    if not os.path.exists(join(args.out_dir, 'labels')):
        os.makedirs(join(args.out_dir, 'labels'))
    # List file
    set_name=''
    if args.train_set:
        set_name = 'train'
    else:
        set_name = 'val'
    list_file = open(join(args.out_dir, set_name+'.txt'), 'w')

    if len(classes) == 0:
        if args.name_file:
            name_f = open(args.name_file)
            for line in name_f:
                classes.append(line.strip('\n'))
        else:
            parse_cls(img_files, args)
            classes.sort()

    for image in img_files:
        if not args.list_only:
            res = convert_annotation(image, args)
            if not res:
                continue
        # If annotation path given but not labels found
        elif args.anno_dir and not os.path.exists(
                join(args.anno_dir, image.split('.')[0] + '.xml')):
            continue
        # Write list file
        list_file.write(join(args.out_dir, 'JPEGImages', image) + '\n')
    list_file.close()

    # Write names file
    print("classes: {}".format(classes))
    with open(join(args.out_dir, 'yolo.names'), 'w') as name:
        for cls in classes:
            name.write('{}\n'.format(cls))
