# import xml.etree.ElementTree as ET
from lxml import etree
import os
from os import listdir, getcwd
from os.path import join
import argparse
import copy

classes = []

def copy_annotation(image, args):
    if args.anno_dir:
        anno_file = join(args.anno_dir, image.split('.')[0]) + '.xml'
    
    if not os.path.isfile(anno_file):
        return False
    # in_file = open(anno_file)
    # tree = ET.parse(in_file)
    # root = tree.getroot()
    root = etree.parse(anno_file)

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    have_obj = False
    for obj in root.iter('object'):
        cls = obj.find('name')
        if cls.text == args.src_label:
            print('Copied '+cls.text)
            new_obj = copy.deepcopy(obj)
            new_cls = new_obj.find('name')
            new_cls.text = args.dst_label
            obj.addnext(new_obj)
        have_obj = True
    etree.ElementTree(root.getroot()).write(anno_file, pretty_print=True)


    return have_obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--anno_dir",
                        help="Directory for VOC annotation xml files")
    parser.add_argument("--src_label",
                        help="Label need to be copied")
    parser.add_argument("--dst_label",
                        help="New label name")
    args = parser.parse_args()

    anno_files = listdir(args.anno_dir)

    for anno in anno_files:
        res = copy_annotation(anno, args)
