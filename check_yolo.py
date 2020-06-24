import os
from os.path import join
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--label_dir',
                    dest='label_dir',
                    type=str,
                    required=True,
                    help='label dir need to be checked')

args = parser.parse_args()

label_dir = os.path.abspath(args.label_dir)

label_list = os.listdir(args.label_dir)

for label in label_list:
    with open(os.path.join(label_dir, label)) as f:
        for line in f:
            contents = line.split(' ')
            if len(contents) != 5:
                continue
            for i in range(1, 5):
                num = float(contents[i])
                if num > 1 or num < 0:
                    print('Error in : ' + os.path.join(label_dir, label))
                    print(line)

