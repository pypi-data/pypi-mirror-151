import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import random

def create_pascal_label_colormap():
    colormap = np.zeros((256, 3), dtype=int)
    ind = np.arange(256, dtype=int)
    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((ind >> channel) & 1) << shift
        ind >>= 3
    return colormap

def label_to_color_image(label):
    if label.ndim != 2:
        raise ValueError('Expect 2-D input label')
    colormap = create_pascal_label_colormap()
    if np.max(label) >= len(colormap):
        raise ValueError('label value too large.')
    return colormap[label]

def vis_segmentation(image, seg_map, name='demo.jpg', if_save=False, if_show=True):

    seg_image = label_to_color_image(seg_map).astype(np.uint8)
    plt.figure()
    plt.imshow(image)
    plt.imshow(seg_image, alpha=0.7)
    plt.axis('off')

    if if_save:
        plt.savefig("vis_{}".format(name))

    if if_show:
        plt.show()

def random_paste(im: np.ndarray, seg: np.ndarray):

    contours, _ = cv2.findContours(seg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        cn_area = [cv2.contourArea(cn) for cn in contours]
        max_cont = contours[cn_area.index(np.max(cn_area))]

        xmin, ymin, w_, h_ = cv2.boundingRect(max_cont)
        xmax = xmin + w_
        ymax = ymin + h_

        seg_roi = seg[ymin:ymax, xmin:xmax]
        img_roi = im[ymin:ymax, xmin:xmax]

        roi = cv2.add(img_roi, np.zeros(np.shape(img_roi), dtype=np.uint8), mask=seg_roi)
        roi_h, roi_w = roi.shape[:2]

        bgh = 0
        bgw = 0
        while not ((roi_h < bgh) & (roi_w < bgw)):
            # bg_index = random.randint(0, len(self.hard_bglist) - 1)
            hard_im_path = 'xx'
            if input_type == 'rgb':
                bgm = cv2.imdecode(np.fromfile(hard_im_path, dtype=np.uint8), 1)
            else:
                bgm = cv2.imdecode(np.fromfile(hard_im_path, dtype=np.uint8), 0)

            bgh, bgw = bgm.shape[:2]
        
        tmp_list = [bgh / roi_h, bgw / roi_w]
