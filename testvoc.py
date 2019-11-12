import cv2
import xml.etree.ElementTree as ET
import os
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--anno_dir", help="Path to annotation directory")
    parser.add_argument("--pic_dir", help="Path to pictures directory")
    args = parser.parse_args()

    labels = os.listdir(args.anno_dir)
    for l in labels:
        name = l.split('.')[0]
        print(name)
        tree = ET.ElementTree(file='out/'+l)
        root = tree.getroot()
        img = cv2.imread(os.path.join(args.pic_dir, name +
                        '.jpeg'))
        for obj in root.findall('object'):
            xmin = int(obj.find('bndbox').find('xmin').text)
            ymin = int(obj.find('bndbox').find('ymin').text)
            xmax = int(obj.find('bndbox').find('xmax').text)
            ymax = int(obj.find('bndbox').find('ymax').text)
            name = obj.find('name').text

            img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255))

            img = cv2.putText(img, name, (xmin, ymin-5), 0, 0.5, (255,0,0))
        cv2.imshow('test', img)
        key = cv2.waitKey(0)
        if key == 27:
            exit()