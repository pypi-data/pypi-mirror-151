# -*- coding: utf-8 -*-
# Created on 8月-31-21 10:21
# @site: https://github.com/moyans
# @author: moyan
import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join

class VOC2YOLO:
    def __init__(self, classes=['person', 'car']):
        self.classes = classes

    def convert(self, size, box):
        dw = 1./(size[0])
        dh = 1./(size[1])
        x = (box[0] + box[1])/2.0 - 1
        y = (box[2] + box[3])/2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x,y,w,h)

    def convert_annotation(self, xml_file, save_txt_path):

        out_file = open(save_txt_path, 'w')
        tree = ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in self.classes or int(difficult)==1:
                continue
            cls_id = self.classes.index(cls)
            xmlbox = obj.find('bndbox')
            xmin = float(xmlbox.find('xmin').text) 
            xmax = float(xmlbox.find('xmax').text) 
            ymin = float(xmlbox.find('ymin').text)
            ymax = float(xmlbox.find('ymax').text)
            if xmax <= xmin: continue
            if ymax <= ymin: continue
            b = (xmin, xmax, ymin, ymax)
            bb = self.convert((w,h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def main():
    classes = ['aeroplane', 'bicycle', 'bird', 'boat',
                'bottle', 'bus', 'car', 'cat', 'chair',
                'cow', 'diningtable', 'dog', 'horse',
                'motorbike', 'person', 'pottedplant',
                'sheep', 'sofa', 'train', 'tvmonitor']

    voc2yolo = VOC2YOLO(classes=classes)

if __name__ == '__main__':
    main()