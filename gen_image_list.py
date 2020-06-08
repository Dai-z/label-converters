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
parser.add_argument('--out_dir',
                    dest='out_dir',
                    type=str,
                    default='',
                    help='generae list file to out_dir, \
                        or the parent dir of image_dir if not given')
parser.add_argument(
    '--set',
    dest='set',
    type=str,
    choices=['train', 'val', 'both'],
    default='train',
    help='generate train.txt or val.txt, or both of them with a ratio of 8:2')

args = parser.parse_args()

image_dir = os.path.abspath(args.image_dir)
image_list = os.listdir(args.image_dir)
if args.out_dir == '':
    out_dir = join(args.image_dir, '..')
else:
    out_dir = args.out_dir
out_dir = os.path.abspath(out_dir)

if args.set != 'both':
    with open(join(out_dir, args.set + '.txt'), 'w') as f:
        for name in image_list:
            line = join(image_dir, name)
            # If can't find annotation
            if not os.path.isfile(
                    line.replace('images', 'annotations').replace(
                        'JPEGImages', 'annotations').replace(
                            '.jpg', '.xml').replace('.png', '.xml')):
                continue
            line += '\n'
            f.write(line)
else:
    with open(join(out_dir, 'train.txt'), 'w') as train, \
        open(join(out_dir, 'val.txt'), 'w') as val:
        for name in image_list:
            line = join(image_dir, name)
            # If can't find annotation
            if not os.path.isfile(
                    line.replace('images', 'annotations').replace(
                        'JPEGImages', 'annotations').replace(
                            '.jpg', '.xml').replace('.png', '.xml')):
                continue
            line += '\n'
            if random.random() < 0.8:
                train.write(line)
            else:
                val.write(line)
