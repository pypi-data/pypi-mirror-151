#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   vis_mask.py
@Time    :   2022/05/06 16:34:46
@Author  :   Moyan 
'''
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_mask(img, seg_map, palette=None, show=False, classes_num=256, opacity=0.5, out_file=None):
    def init_palette():
        state = np.random.get_state()
        np.random.seed(42)
        palette = np.random.randint(0, 255, size=(classes_num, 3))
        np.random.set_state
        return palette
    img = img.copy()
    img = img[..., ::-1]
    print(np.unique(seg_map))
    if palette is None: palette = init_palette()
    color_seg = np.zeros((seg_map.shape[0], seg_map.shape[1], 3), dtype=np.uint8)
    for label, color in enumerate(palette):
        # print(label, color)
        color_seg[seg_map==label, :] = color
    # convert to BGR
    color_seg = color_seg[..., ::-1]

    img = img * (1-opacity) + color_seg * opacity
    img = img.astype(np.uint8)

    plt.figure()
    plt.imshow(img)
    plt.axis('off')

    if show:
        plt.show()
    if out_file is not None:
        cv2.imwrite(out_file, img)

    plt.close()

# def main():
#     img_path = r"D:\Code\sunc\generate_fake_idcard\gen_xj_0_front.jpg"
#     mask_path = r"D:\Code\sunc\generate_fake_idcard\gen_xj_0_front.png"
#     im = cv2.imread(img_path)
#     mask = cv2.imread(mask_path, 0)

#     out_file = "vis.png"
#     show_mask(im, mask, show=True, out_file=out_file)
# if __name__ == '__main__':
#     main()
