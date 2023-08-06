# -*- coding: utf-8 -*-
# Created on Mar-14-22 17:32
# @site: https://github.com/moyans
# @author: moyan
import os
import random
from PIL import Image
import numpy as np
from collections import namedtuple

cls_template = namedtuple('cls', ['name', 'id', 'color'])
# label_key_val_map = [
#     cls_template('bg', 0, (0, 0, 0)),
#     cls_template('cls1', 1, (255, 128, 128)),
#     cls_template('cls2', 2, (255, 255, 128)),
#     cls_template('cls3', 3, (128, 255, 128)),
#     cls_template('cls4', 4, (128, 255, 255)),
#     cls_template('cls5', 5, (0, 128, 255)),
#     cls_template('cls6', 6, (255, 0, 0)),
#     cls_template('cls7', 7, (0, 128, 192)),
#     cls_template('cls8', 8, (255, 0, 255)),
#     cls_template('cls9', 9, (255, 128, 64)),
#     cls_template('cls10', 10, (128, 64, 0)),
#     cls_template('cls11', 11, (128, 128, 0)),
# ]

label_key_val_map = [
    cls_template('bg', 0, (0, 0, 0)),
    cls_template('back_all', 9, (255, 128, 128)),
    cls_template('back_organize', 7, (255, 255, 128)),
    cls_template('back_effetive_data', 6, (128, 255, 128)),
    cls_template('front_all', 8, (128, 255, 255)),
    cls_template('front_name', 1, (0, 128, 255)),
    cls_template('front_gender', 2, (255, 0, 0)),
    cls_template('front_nation', 3, (0, 128, 192)),
    cls_template('front_addr', 4, (255, 0, 255)),
    cls_template('front_idnum', 5, (255, 128, 64)),
]


def get_putpalette(Clss, color_other=[0, 0, 0]):
    '''
    灰度图转8bit彩色图
    :param Clss:颜色映射表
    :param color_other:其余颜色设置
    :return:
    '''
    putpalette = []
    for cls in Clss:
        putpalette += list(cls.color)
    putpalette += color_other * (255 - len(Clss))
    return putpalette

def main():

    gray_mask_path = 'demo.png'
    gray_8bit_mask_path = 'demo_8bit.png'

    src = Image.open(gray_mask_path)
    mat = np.array(src, dtype=np.uint8)
    dst = Image.fromarray(mat, 'P')

    bin_colormap = get_putpalette(label_key_val_map)
    dst.putpalette(bin_colormap)
    dst.save(gray_8bit_mask_path)
    src.close()

def batch_dir():

    img_dir = r"D:\Code\sunc\generate_fake_idcard\res\xj\mask"
    save_dir = os.path.join(os.path.dirname(img_dir), "mask8bit")
    if not os.path.exists(save_dir): os.makedirs(save_dir)

    img_list = os.listdir(img_dir)
    for ind, names in enumerate(img_list):
        if ind%100 == 0: print(ind, names)
        name, suffix = os.path.splitext(names)
        if suffix != ".png":continue
        gray_mask_path = os.path.join(img_dir, name+".png")
        mask8bit_path = os.path.join(save_dir, name+".png")
        # mask = cv2.imread(mask_path)
        # new_mask = encode_segmap(mask)
        # cv2.imwrite(mask_path, new_mask)

        src = Image.open(gray_mask_path)
        mat = np.array(src, dtype=np.uint8)
        dst = Image.fromarray(mat, 'P')

        bin_colormap = get_putpalette(label_key_val_map)
        dst.putpalette(bin_colormap)
        dst.save(mask8bit_path)
        src.close()

    
if __name__ == '__main__':
    # main()
    batch_dir()