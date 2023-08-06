#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
import os
import sys
import json
import time
import random
import operator
from copy import deepcopy
from difflib import SequenceMatcher
from collections import namedtuple

from . import UtilsCommon as utils
from .UtilsCommon import screen_height, screen_width

basename = os.path.basename(__file__)
try:
    # noinspection PyUnresolvedReferences
    import imutils
except Exception as e:
    print(" @ Warning: imutils import error in {} - {}".format(basename, str(e)))
try:
    # noinspection PyUnresolvedReferences
    import cv2
    CV2_FONT = cv2.FONT_HERSHEY_SIMPLEX
    CV2_INTER_AREA = cv2.INTER_AREA
except Exception as e:
    print(" @ Warning: cv2 import error in {} - {}".format(basename, str(e)))
    CV2_FONT = None
    CV2_INTER_AREA = None
try:
    # noinspection PyUnresolvedReferences
    import numpy as np
except Exception as e:
    print(" @ Warning: numpy import error in {} - {}".format(basename, str(e)))
try:
    # noinspection PyUnresolvedReferences
    from PIL import Image
except Exception as e:
    print(" @ Warning: PIL.Image import error in {} - {}".format(basename, str(e)))
try:
    # noinspection PyUnresolvedReferences
    import matplotlib.pyplot as plt
except Exception as e:
    print(" @ Warning: matplotlib import error in {} - {}".format(basename, str(e)))


_this_folder_ = os.path.dirname(os.path.abspath(__file__))

RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
CYAN    = (  0, 255, 255)
MAGENTA = (255,   0, 255)
YELLOW  = (255, 255,   0)
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)

cvRED     = BLUE
cvGREEN   = GREEN
cvBLUE    = RED
cvCYAN    = YELLOW
cvMAGENTA = MAGENTA
cvYELLOW  = CYAN
cvWHITE   = WHITE
cvBLACK   = BLACK

COLOR_ARRAY_RGB      = [RED, GREEN, BLUE]
COLOR_ARRAY_RGBKW    = [RED, GREEN, BLUE, BLACK, WHITE]
COLOR_ARRAY_RGBCMY   = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]
COLOR_ARRAY_RGBCMYKW = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, BLACK, WHITE]

cvCOLOR_ARRAY_RGB      = [cvRED, cvGREEN, cvBLUE]
cvCOLOR_ARRAY_RGBKW    = [cvRED, cvGREEN, cvBLUE, cvBLACK, cvWHITE]
cvCOLOR_ARRAY_RGBCMY   = [cvRED, cvGREEN, cvBLUE, cvCYAN, cvMAGENTA, cvYELLOW]
cvCOLOR_ARRAY_RGBCMYKW = [cvRED, cvGREEN, cvBLUE, cvCYAN, cvMAGENTA, cvYELLOW, cvBLACK, cvWHITE]

'''
HANGUL_FONT = os.path.join(_this_folder_, "Fonts", "SourceHanSerifK-Regular.otf")
HANGUL_FONT_GULIM = os.path.join(_this_folder_, "Fonts", "gulim.ttf")
HANGUL_FONT_GMARKET = os.path.join(_this_folder_, "Fonts", "GmarketSansMedium.otf")
HANGUL_FONT_IMCRE = os.path.join(_this_folder_, "Fonts", "ImcreSoojin OTF.otf")
HANGUL_FONT_TMONEY = os.path.join(_this_folder_, "Fonts", "TmoneyRoundWindRegular.otf")
'''


class LoggerWrapper:

    def info(self): pass

    def error(self): pass


def get_stdout_logger(logger=None):
    if logger is None:
        logger = LoggerWrapper()
        logger.info = print
        logger.error = print
    return logger


def imread(img_file, color_fmt='RGB'):
    """
    Read image file.
    Support gif and pdf format.

    :param  img_file:
    :param  color_fmt: RGB, BGR, or GRAY. The default is RGB.
    :return img:
    """
    if not isinstance(img_file, str):
        # print(" % Warning: input is NOT a string for image filename")
        return img_file

    if not os.path.exists(img_file):
        print(" @ Error: image file not found {}".format(img_file))
        sys.exit()

    if not (color_fmt == 'RGB' or color_fmt == 'BGR' or color_fmt == 'GRAY'):
        color_fmt = 'RGB'

    if img_file.split('.')[-1] == 'gif':
        gif = cv2.VideoCapture(img_file)
        ret, img = gif.read()
        if not ret:
            return None
    elif img_file.split('.')[-1] == 'pdf':
        img = read_pdf(img_file, resolution=300)
    else:
        # img = cv2.imread(img_file.encode('utf-8'))
        # img = cv2.imread(img_file)
        # img = np.array(Image.open(img_file.encode('utf-8')).convert('RGB'), np.uint8)
        img = np.array(Image.open(img_file).convert('RGB'), np.uint8)

    if color_fmt.upper() == 'GRAY':
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    elif color_fmt.upper() == 'BGR':
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    else:
        return img


def read_pdf(pdf_filename, resolution=300):
    img_filename = 'temp.bmp'
    convert_pdf_to_img(pdf_filename, 'bmp', img_filename, resolution=resolution)
    img = imread(img_filename, color_fmt='RGB')
    os.remove(img_filename)
    return img


def imwrite(img, img_fname, color_fmt='RGB'):
    """
    write image file.

    :param img:
    :param img_fname:
    :param  color_fmt: RGB, BGR, or GRAY. The default is RGB.
    :return img:
    """
    if color_fmt == 'RGB':
        tar = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif color_fmt == 'GRAY':
        tar = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif color_fmt == 'BGR':
        tar = img[:]
    else:
        print(" @ Error: color_fmt, {}, is not correct.".format(color_fmt))
        return False

    cv2.imwrite(img_fname, tar)
    return True


def imresize(img, width=None, height=None, interpolation=CV2_INTER_AREA):
    """
    resize image.

    :param img:
    :param width:
    :param height:
    :param interpolation:
    :return:
    """
    h, w, _ = img.shape

    if width is None and height is None:
        return img

    elif w == width and h == height:
        return img

    elif width is None:
        ratio = height / h
        width = int(w * ratio)
        return cv2.resize(img, (width, height), interpolation)

    elif height is None:
        ratio = width / w
        height = int(h * ratio)
        return cv2.resize(img, (width, height), interpolation)

    else:
        return cv2.resize(img, (width, height), interpolation)


def imshow(img, desc='imshow', zoom=1.0, color_fmt='RGB', skip=False, pause_sec=0, loc=(64,64)):
    """
    :param img:
    :param desc:
    :param zoom:
    :param color_fmt:
    :param skip:
    :param pause_sec:
    :param loc:
    :return:
    """
    pause_sec = -1 if pause_sec is None else pause_sec
    if skip or pause_sec < 0:
        return

    if isinstance(img, str):
        img = imread(img)

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif len(img.shape) == 3 and color_fmt == 'RGB':
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # def get_full_zoom_factor(img, zoom=0.0, factor=4/5., skip_=False):

    dim = img.shape
    h, w = dim[0], dim[1]
    zoom_w = screen_width  / float(w) * 8/10.
    zoom_h = screen_height / float(h) * 8/10.

    if zoom == 0:
        zoom = min(zoom_h, zoom_w)
    elif (screen_width < w * zoom) or (screen_height < h * zoom):
        zoom = min(zoom_h, zoom_w)
    else:
        pass

    resize_img = cv2.resize(img, (0, 0), fx=zoom, fy=zoom)

    if os.environ.get('XSERVER'):
        if os.environ['XSERVER'] == 'False':
            imwrite(resize_img, os.path.join(os.environ['HOME'], "Downloads", "imwrite.jpg"), color_fmt='BGR')
            print("imwrite instead of imshow")
            return

    try:
        cv2.imshow(desc, resize_img)
        if loc[0] >= 0 and loc[1] >= 0:
            cv2.moveWindow(desc, loc[0], loc[1])
        if pause_sec == 0:
            cv2.waitKey()
        else:
            cv2.waitKey(int(pause_sec * 1000))
        cv2.waitKey(1)
        cv2.destroyWindow(desc)
        for k in range(10):
            cv2.waitKey(1)
    except Exception as err:
        print(err)
        plt.axis("off")
        plt.imshow(resize_img)
        if pause_sec == 0:
            plt.show()
        else:
            plt.draw()
            plt.pause(pause_sec)
        plt.close()


def convert_pdf_to_img(pdf_filename, img_type, img_filename, resolution=300):
    if os.name == 'nt':
        print(" @ Error: Wand library does not work in Windows OS\n")
        sys.exit()
    else:
        # noinspection PyUnresolvedReferences
        from wand.image import Image
        with Image(filename=pdf_filename, resolution=resolution) as img:
            img.compression = 'no'
            with img.convert(img_type) as converted:
                converted.save(filename=img_filename)


def read_all_images(img_dir,
                    prefix='',
                    exts=None,
                    color_fmt='RGB'):
    """
    Read all images with specific filename prefix in an image directory.

    :param img_dir:
    :param prefix:
    :param exts:
    :param color_fmt:
    :color_fmt:
    :return imgs: image list
    """
    if exts is None:
        exts = utils.IMG_EXTENSIONS
    imgs = []

    filenames = os.listdir(img_dir)
    filenames.sort()

    for filename in filenames:
        if filename.startswith(prefix) and os.path.splitext(filename)[-1][1:] in exts:
            img = imread(os.path.join(img_dir, filename), color_fmt=color_fmt)
            imgs.append(img)

    if not imgs:
        print(" @ Error: no image filename starting with \"{}\"...".format(prefix))
        sys.exit()

    return imgs


def imread_all_images(img_path,
                      fname_prefix='',
                      img_extensions=None,
                      color_fmt='RGB'):
    """
    Read all images in the specific folder.

    :param img_path:
    :param fname_prefix:
    :param img_extensions:
    :param color_fmt:
    :return imgs: image list
    """
    if img_extensions is None:
        img_extensions = utils.IMG_EXTENSIONS

    img_filenames = []
    imgs = []

    if os.path.isfile(img_path):
        filenames = [img_path]
    elif os.path.isdir(img_path):
        filenames = [os.path.join(img_path, x) for x in os.listdir(img_path)]
    else:
        print(" @ Error: The input argument is NOT a file nor folder.\n")
        return [], []

    filenames.sort()
    for filename in filenames:
        if os.path.splitext(filename)[1][1:] in img_extensions:
            if os.path.basename(filename).startswith(fname_prefix):
                imgs.append(imread(filename, color_fmt=color_fmt))
                img_filenames.append(filename)

    return imgs, img_filenames


def vstack_images(imgs, margin=20):
    """
    Stack images vertically with boundary and in-between margin.

    :param imgs:
    :param margin:
    :return:
    """
    widths = []
    heights = []
    num_imgs = len(imgs)

    if num_imgs == 1:
        return imgs[0]

    color_images = []
    for img in imgs:
        img_sz = img.shape[1::-1]
        widths.append(img_sz[0])
        heights.append(img_sz[1])
        color_images.append(img)

    max_width = max(widths) + 2 * margin
    max_height = sum(heights) + (num_imgs + 1) * margin
    if len(imgs[0].shape) == 3:
        vstack_image = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    else:
        vstack_image = np.zeros((max_height, max_width), dtype=np.uint8)

    x_offset = margin
    y_offset = margin
    for img in color_images:
        img_sz = img.shape[1::-1]
        vstack_image[y_offset:y_offset + img_sz[1], x_offset:x_offset + img_sz[0]] = img
        y_offset += margin + img_sz[1]

    return vstack_image


def hstack_images(imgs, margin=20):
    """
    Stack images horizontally with boundary and in-between margin.

    :param imgs:
    :param margin:
    :return:
    """
    widths = []
    heights = []
    num_imgs = len(imgs)

    if num_imgs == 1:
        return imgs[0]

    color_images = []
    for img in imgs:
        img_sz = img.shape[1::-1]
        widths.append(img_sz[0])
        heights.append(img_sz[1])
        color_images.append(img)

    max_width = sum(widths) + (num_imgs + 1) * margin
    max_height = max(heights) + 2 * margin
    if len(imgs[0].shape) == 3:
        hstack_image = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    else:
        hstack_image = np.zeros((max_height, max_width), dtype=np.uint8)

    x_offset = margin
    y_offset = margin
    for img in color_images:
        img_sz = img.shape[1::-1]
        hstack_image[y_offset:y_offset + img_sz[1], x_offset:x_offset + img_sz[0]] = img
        x_offset += margin + img_sz[0]

    return hstack_image


#################


def find_four_corners(img):
    normalized_img = normalize_image(img)
    gray = cv2.cvtColor(normalized_img, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.medianBlur(gray, 11)
    retval, thresh_gray = cv2.threshold(blurred_image, thresh=240, maxval=255, type=cv2.THRESH_BINARY_INV)
    rsz_img = cv2.resize(thresh_gray, (0, 0), fx=0.3, fy=0.3)
    cv2.imshow("four corners", rsz_img)
    cv2.waitKey(0)
    points = np.argwhere(thresh_gray == 0)
    points = np.fliplr(points)
    x1, y1, w, h = cv2.boundingRect(points)
    x2 = x1 + w
    y2 = y1 + h
    return x1, x2, y1, y2


def line_removal(img):
    """

    :param img:
    :return:
    """

    if img is None:
        print("Image is empty!")
        pass

    imshow(img, desc="Original image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imshow(gray, desc="Gray image")

    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    imshow(bw, desc="Binary image")

    hz = bw
    vt = bw

    hz_size = hz.shape[1] / 30
    hz_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (hz_size, 1, 1))
    hz = cv2.erode(hz, hz_structure, iterations=1)
    hz = cv2.dilate(hz, hz_structure, iterations=1)
    imshow(hz, desc="horizontal")

    vt_size = vt.shape[0] / 30
    vt_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vt_size, 1))
    vt = cv2.erode(vt, vt_structure, iterations=1)
    vt = cv2.dilate(vt, vt_structure, iterations=1)
    imshow(vt, desc="vertical")

    # bitwise_not
    vt = cv2.bitwise_not(vt)
    imshow(vt, desc="vertical bit")

    """
    Extract edges and smooth image according to the logic
    1. extract edges
    2. dilate(edges)
    3. src.copyTo(smooth)
    4. blur smooth img
    5. smooth.copyTo(src, edges)
    """

    edges = cv2.adaptiveThreshold(vt, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -2)
    imshow(edges, desc="edges")

    kernel = np.ones((2, 2), dtype="uint8")
    edges = cv2.dilate(edges, kernel)
    imshow(edges, desc="dilated edges")

    smoothing = vt
    smoothing = cv2.blur(smoothing, (2, 2, 1))
    vt, edges = smoothing
    imshow(vt, desc="smooth")


def plot_dots(img, coord_list):
    for coordinates in coord_list:
        cv2.circle(img, coordinates, 15, (15, 15, 255), thickness=10)
    return img


def normalize_image(img):
    min_val = np.min(img)
    max_val = np.max(img)
    normalized_img = ((img - min_val) / (max_val - min_val)) * 255.
    return np.uint8(normalized_img)


def find_black_rects(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY)
    # rsz_img = cv2.resize(thresh_gray, (0, 0), fx=0.3, fy=0.3)
    # cv2.imshow("result", rsz_img)
    # cv2.waitKey(0)

    cv2.bitwise_not(thresh_gray, thresh_gray)
    _, contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    for cont in contours:
        x1, y1, w, h = cv2.boundingRect(cont)
        k = float(h)/w
        if 0.9 < k < 1.1 and 1000 < w*h < 1500:
            cv2.drawContours(img, contours, i, (0,250,0), thickness=10)

        i += 1
    imshow(img)
    # rsz_img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
    # cv2.imshow("result", rsz_img)
    # cv2.waitKey(0)


def detect_four_corners_based_on_ref_squares(img,
                                             ref_vertex,
                                             search_margin=0.1,
                                             square_width=50./2480,
                                             debug_=False):
    """
    Detect four quadrilateral vertices based on reference black squares.
    It is assumed that four black squares are located
    near the four corners based on reference vertices.

    :param img:
    :param ref_vertex:
    :param search_margin:
    :param square_width:
    :param debug_:
    :return: status, detected vertices, output image
    """
    square_ratio_range = [0.8, 1.2]
    square_width_margin = 0.5
    square_fill_thresh = 0.8

    debug_in_ = False

    dim = img.shape[1::-1]
    square_width = square_width * dim[0]
    real_vertices = generate_four_vertices_from_ref_vertex(ref_vertex, dim)
    crop_boxes = []
    offsets = [int(x*search_margin) for x in dim]
    crop_boxes.append([real_vertices[0][0],            real_vertices[0][1],
                       real_vertices[0][0]+offsets[0], real_vertices[0][1]+offsets[1]])
    crop_boxes.append([real_vertices[1][0]-offsets[0], real_vertices[1][1],
                       real_vertices[1][0],            real_vertices[1][1]+offsets[1]])
    crop_boxes.append([real_vertices[2][0],            real_vertices[2][1]-offsets[1],
                       real_vertices[2][0]+offsets[0], real_vertices[2][1]])
    crop_boxes.append([real_vertices[3][0]-offsets[0], real_vertices[3][1]-offsets[1],
                       real_vertices[3][0],            real_vertices[3][1]])

    detected_vertices = []
    kernel = np.ones((5,5),np.uint8)
    for idx in range(4):
        crop_img = img[crop_boxes[idx][1]:crop_boxes[idx][3], crop_boxes[idx][0]:crop_boxes[idx][2]]
        gray_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
        ret, thresh_gray = cv2.threshold(gray_img,
                                         thresh=200,
                                         maxval=255,
                                         # type=cv2.THRESH_BINARY)
                                         type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        for _ in range(3):
            thresh_gray = cv2.morphologyEx(thresh_gray, cv2.MORPH_CLOSE, kernel)
        cv2.bitwise_not(thresh_gray, thresh_gray)
        thresh_color = cv2.cvtColor(thresh_gray, cv2.COLOR_GRAY2RGB)
        ret, contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_width_ratio = 1
        det_vertex = []
        for i, cont in enumerate(contours):
            x1, y1, w, h = cv2.boundingRect(cont)
            ratio = h/w
            width_ratio = abs(square_width - w) / square_width
            if debug_in_:
                if w > 10 and h > 10:
                    # cv2.drawContours(crop_img, contours, i, GREEN, thickness=4)
                    cv2.drawContours(thresh_color, contours, i, GREEN, thickness=4)
                    print("-------")
                    print(i)
                    print(x1, y1, w, h, width_ratio)
                    print(ratio, cv2.contourArea(cont)/(w*h))

            if square_ratio_range[0] < ratio < square_ratio_range[1] and \
                    width_ratio < square_width_margin and \
                    cv2.contourArea(cont) / (w*h) > square_fill_thresh:
                moments = cv2.moments(cont)
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
                if width_ratio < min_width_ratio:
                    det_vertex = [cx + crop_boxes[idx][0], cy + crop_boxes[idx][1]]
                    min_width_ratio = width_ratio
                    # print("****")
                if debug_:
                    disp_img = np.copy(crop_img)
                    cv2.drawContours(disp_img, contours, i, RED, thickness=4)
                    cv2.circle(disp_img,(cx, cy), 8, GREEN, -1)
                    imshow(disp_img)
        if debug_in_:
            imshow(thresh_color, desc="thresh_color")
        if det_vertex:
            detected_vertices.append(det_vertex)
    box_img = np.copy(img)
    if len(detected_vertices) != 4:
        # print(" @ Error: 4 corners are NOT  detected!")
        return False, detected_vertices, img

    cv2.line(box_img, tuple(detected_vertices[0]), tuple(detected_vertices[1]), RED, 10)
    cv2.line(box_img, tuple(detected_vertices[0]), tuple(detected_vertices[2]), RED, 10)
    cv2.line(box_img, tuple(detected_vertices[1]), tuple(detected_vertices[3]), RED, 10)
    cv2.line(box_img, tuple(detected_vertices[2]), tuple(detected_vertices[3]), RED, 10)
    if debug_:
        imshow(box_img, desc="four corners")

    return True, detected_vertices, img


def draw_line_from_rho_and_theta(img, rho, theta, pause_sec=-1):

    img_sz = img.shape[1::-1]
    a, b = np.cos(theta), np.sin(theta)
    x0, y0 = a * rho, b * rho
    x = []
    y = []
    if b != 0:
        slope = -a / b
        y1 = slope * (-x0) + y0
        if 0 <= y1 < img_sz[1]:
            x.append(0)
            y.append(y1)
        y1 = slope * (img_sz[0] - 1 - x0) + y0
        if 0 <= y1 < img_sz[1]:
            x.append(img_sz[0] - 1)
            y.append(y1)
        x1 = (-y0) / slope + x0
        if 0 <= x1 < img_sz[0]:
            x.append(x1)
            y.append(0)
        x1 = (img_sz[1] - 1 - y0) / slope + x0
        if 0 <= x1 < img_sz[0]:
            x.append(x1)
            y.append(img_sz[1] - 1)
    else:
        x = [x0, x0]
        y = [0, img_sz[1]-1]
    angle = (90 - (theta * 180 / np.pi))
    if pause_sec >= 0:
        print(" # rotated angle = {:f} <- ({:.3f}, {:.3f})".format(angle, theta, rho))
    if len(x) == 2:
        pts = [[int(x[0]+0.5), int(y[0]+0.5)], [int(x[1]+0.5), int(y[1]+0.5)]]
    else:
        if pause_sec >= 0:
            print(" @ Warning: rho is zero.\n")
        pts = [[0,0],[0,0]]

    line_img = np.copy(img)
    cv2.line(line_img, (pts[0][0], pts[0][1]), (pts[1][0], pts[1][1]), RED, 4)
    imshow(line_img, pause_sec=pause_sec)

    return pts


def check_lines_in_img(img, algorithm='HoughLineTransform'):

    if img.shape != 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_rgb = np.copy(img)
    else:
        img_gray = np.copy(img)
        img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)

    ret, img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_edge = cv2.Canny(img_bw, 50, 150, apertureSize=3)

    if algorithm == 'HoughLineTransform':

        lines = cv2.HoughLines(img_edge, 1, np.pi/180, 100)
        print(" # Total lines: {:d}".format(len(lines)))
        for line in lines:
            img_lines = np.copy(img_rgb)
            dim = img_lines.shape
            rho = line[0][0]
            theta = line[0][1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x = []
            y = []
            if b != 0:
                slope = -a / b
                y1 = slope * (-x0) + y0
                if 0 <= y1 < dim[0]:
                    x.append(0)
                    y.append(y1)
                y1 = slope * (dim[1] - 1 - x0) + y0
                if 0 <= y1 < dim[0]:
                    x.append(dim[1] - 1)
                    y.append(y1)
                x1 = (-y0) / slope + x0
                if 0 <= x1 < dim[1]:
                    x.append(x1)
                    y.append(0)
                x1 = (dim[0] - 1 - y0) / slope + x0
                if 0 <= x1 < dim[1]:
                    x.append(x1)
                    y.append(dim[0] - 1)
            else:
                x = [x0, x0]
                y = [0, dim[0]-1]
            angle = (90 - (theta * 180 / np.pi))
            print(" # rotated angle = {:.1f} <- ({:f}, {:f})".format(angle, theta, rho))
            if len(x) == 2:
                img_lines = cv2.line(img_rgb, (int(x[0]), int(y[0])), (int(x[1]), int(y[1])), RED, 4)
                plt_imshow(img_lines)
                # if -5 < angle < 0 or 0 < angle < 5:
                #     plt_imshow(img_line)
            else:
                print(" @ Warning: something wrong.\n")
                pass

    elif algorithm == 'ProbabilisticHoughTransform':
        end_pts_list = cv2.HoughLinesP(img_edge, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=50)
        img_lines = np.copy(img_rgb)
        print(" # Total lines: {:d}".format(len(end_pts_list)))
        for end_pts in end_pts_list:
            cv2.line(img_lines, tuple(end_pts[0][0:2]), tuple(end_pts[0][2:]), RED, 10)
            angle = np.arctan2(end_pts[0][3]-end_pts[0][1], end_pts[0][2]-end_pts[0][0]) * 180. / np.pi
            print(" # rotated angle = {:.1f}".format(angle))
            imshow(img_lines)
        # if -5 < angle < 0 or 0 < angle < 5:
        #     plt_imshow(img_line)

    return True


def derotate_image(img,
                   max_angle=30,
                   max_angle_candidates=50,
                   angle_resolution=0.5,
                   inside_margin_ratio=0.1,
                   rot_img_fname=None,
                   check_time_=False,
                   pause_img_sec=-1):
    """
    Derotate image.

    :param img:
    :param max_angle: Maximum rotated angle. The angles above this should be ignored.
    :param max_angle_candidates:
    :param angle_resolution:
    :param inside_margin_ratio:
    :param rot_img_fname:
    :param check_time_:
    :param pause_img_sec:
    :return:
    """
    start_time = None
    if check_time_:
        start_time = time.time()
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img_gray = np.amin(img, axis=2)
    else:
        img_gray = np.copy(img)

    inside_margin = [int(x * inside_margin_ratio) for x in img.shape[1::-1]]

    img_gray[ :inside_margin[1],:] = 255
    img_gray[-inside_margin[1]:,:] = 255
    img_gray[:, :inside_margin[0]] = 255
    img_gray[:,-inside_margin[0]:] = 255

    # noinspection PyUnreachableCode
    if False:
        check_lines_in_img(img, algorithm='HoughLineTransform')
        check_lines_in_img(img, algorithm='ProbabilisticHoughTransform')

    ret, img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    """
    kernel = np.ones((5, 5), np.uint8)  # note this is a horizontal kernel
    bw = np.copy(img_bw)
    for i in range(9):
        bw = cv2.erode(bw, kernel, iterations=1)
        bw = cv2.dilate(bw, kernel, iterations=1)
    imshow(hstack_images((img_bw, bw)))
    """
    img_edge = cv2.Canny(img_bw, 50, 150, apertureSize=3)

    # noinspection PyUnreachableCode
    if False:
        imshow(img_edge)
        # plt_imshow(edges)

    lines = cv2.HoughLines(img_edge, 1, np.pi/360, int(min(img_edge.shape)/8.))

    angles = []
    if lines is not None:
        for cnt, line in enumerate(lines):
            angle = int((90 - line[0][1] * 180 / np.pi) / float(angle_resolution)) * angle_resolution
            draw_line_from_rho_and_theta(img, line[0][0], line[0][1], pause_sec=-1)

            if abs(angle) < max_angle:
                angles.append(angle)
            if max_angle_candidates < cnt:
                break

    # rot_angle = max(set(angles), key=angles.count)
    sorted_angles = sorted({x:angles.count(x) for x in angles}.items(), key=operator.itemgetter(1), reverse=True)

    if len(sorted_angles) == 0:
        rot_angle = 0
    elif len(sorted_angles) == 1:
        rot_angle = sorted_angles[0][0]
    elif sorted_angles[0][0] == 0 and (sorted_angles[0][1] < 2 * sorted_angles[1][1]):
        rot_angle = sorted_angles[1][0]
    elif (sorted_angles[0][1] / sorted_angles[1][1]) < 3 and abs(sorted_angles[0][0] - sorted_angles[1][0]) <= 1.0:
        rot_angle = (sorted_angles[0][0] + sorted_angles[1][0]) / 2.
    else:
        rot_angle = sorted_angles[0][0]

    """
    if rot_angle != 0:
        rot_angle += 0.5
    """
    if pause_img_sec >= 0:
        print("# Rotated angle is {:5.1f} degree.".format(rot_angle))

    sz = img_bw.shape[1::-1]
    rot_img = ~imutils.rotate(~img, angle=-rot_angle, center=(int(sz[0]/2), int(sz[1]/2)), scale=1)
    if check_time_:
        print(" # Time for rotation detection and de-rotation if any : {:.2f} sec".
              format(float(time.time() - start_time)))

    if 0 <= pause_img_sec:
        imshow(np.concatenate((img, rot_img), axis=1), pause_sec=pause_img_sec, desc="de-rotation")

    if rot_img_fname:
        imwrite(rot_img_fname, rot_img, 'RGB')

    return rot_img


def erase_lines_in_image(img,
                         check_time_=False,
                         pause_img_sec=-1):
    """
    Erase lines.

    :param img:
    :param check_time_:
    :param pause_img_sec:
    :return:
    """
    erase_window_sz = 9
    line_thresh = 32

    start_time = None
    if check_time_:
        start_time = time.time()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else np.copy(img)
    ret, img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    """
    kernel = np.ones((1, 5), np.uint8)  # note this is a horizontal kernel
    bw = np.copy(img_bw)
    for i in range(9):
        bw = cv2.dilate(bw, kernel, iterations=1)
        bw = cv2.erode(bw, kernel, iterations=1)
    imshow(hstack_images((img_bw, bw)))
    """

    img_edge = cv2.Canny(img_bw, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(img_edge, 1, np.pi/360, 200)
    print(" # Total number of lines detected is {:d}.".format(len(lines)))
    imshow(img_bw, pause_sec=pause_img_sec)

    img_erase = np.ones((img_bw.shape[:2]), dtype=np.uint8) * 255
    for cnt, line in enumerate(lines):
        line_pts = draw_line_from_rho_and_theta(img, line[0][0], line[0][1], pause_sec=pause_img_sec)
        x0, y0, x1, y1 = line_pts[0][0], line_pts[0][1], line_pts[1][0], line_pts[1][1]
        pnts = []
        if (x1 - x0) > (y1 - y0):
            for x in range(x0, x1):
                y = (y1 - y0) / (x1 - x0) * (x - x0) + y0
                pnts.append([int(x), int(y), img_bw[int(y),int(x)]])
        else:
            for y in range(y0, y1):
                x = (x1 - x0) / (y1 - y0) * (y - y0) + x0
                pnts.append([int(x), int(y), img_bw[int(y),int(x)]])
        cnt = 0
        stt_pnt = 0
        for i in range(len(pnts)):
            if pnts[i][2] == 255:
                if cnt == 0:
                    stt_pnt = i
                cnt += 1
            else:
                if cnt > line_thresh:
                    # print(" > {:d}-th line: {:d} + {:d} = {:d}".format(cnt, stt_pnt, cnt, stt_pnt+cnt))
                    for j in range(cnt):
                        pos = pnts[stt_pnt+j][:2]
                        if (x1 - x0) > (y1 - y0):
                            img_erase[pos[1]-erase_window_sz:pos[1]+erase_window_sz+1,pos[0]] = 0
                        else:
                            img_erase[pos[1], pos[0]-erase_window_sz:pos[0]+erase_window_sz+1] = 0
                cnt = 0
        imshow(img_erase, pause_sec=pause_img_sec)

    if check_time_:
        print(" # The processing time of erasing line function is {:.3f} sec".
              format(float(time.time() - start_time)))

    img_bw_erase = ((img_erase == 0) * 0 + (img_erase != 0) * img_bw).astype(np.uint8)

    return img_erase, img_bw_erase


def run__crop():
    paper_size = 'A4'
    ref_dim = [1280, None]

    org_img = imread("test_images/DB_1.jpg")
    ret, det_vertices, box_img = detect_four_corners_based_on_ref_squares(org_img,
                                                                          (0,0),
                                                                          search_margin=0.1,
                                                                          square_width=50./2480,
                                                                          debug_=False)
    if paper_size == 'A4':
        ref_dim[1] = int(ref_dim[0] * np.sqrt(2.))

    tar_vertices = [[0,0], [ref_dim[0],0], [0, ref_dim[1]], [ref_dim[0], ref_dim[1]]]
    mtx = cv2.getPerspectiveTransform(np.float32(det_vertices),np.float32(tar_vertices))
    warp_img = cv2.warpPerspective(org_img, mtx, dsize=tuple(ref_dim), flags=cv2.INTER_LINEAR)
    imshow(warp_img, "output")
    imwrite(warp_img, "output.png")


def run__derotate():

    img_path = 'test_images/census-rotate-2.jpeg'

    imgs, filenames = imread_all_images(img_path, fname_prefix='census-rotate-')
    for img in imgs:
        rot_img = derotate_image(img,
                                 rot_img_fname=None,
                                 check_time_=False,
                                 pause_img_sec=0)
        imshow(np.hstack((img, rot_img)), desc="de-rotation")


def run__erase_lines_in_image():

    img_path = 'test_images/census-1.jpg'
    img_prefix = ''
    imgs, filenames = imread_all_images(img_path, fname_prefix=img_prefix)
    for img in imgs:
        erase_img = erase_lines_in_image(img, pause_img_sec=0)
        imshow(np.hstack((cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), erase_img)), desc="erase lines")


def detect_text_area(img, area_ratio_thresh=0.25, char_min_pxl=10, debug_=False):

    # convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # smooth the image to avoid noises
    filtered = cv2.medianBlur(gray, 3)

    # Apply adaptive threshold
    # thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    _, thresh = cv2.threshold(filtered, thresh=128, maxval=255, type=cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((5,5), np.uint8)
    """
    kernel[0:2,0:2] = 0
    kernel[0:2,3:5] = 0
    kernel[3:5,3:5] = 0
    kernel[3:5,0:2] = 0
    kernel[1,1] = 1
    kernel[1,3] = 1
    kernel[3,1] = 1
    kernel[3,3] = 1
    """

    morph = np.copy(thresh)
    for _ in range(5):
        morph = cv2.dilate(morph, kernel, iterations=3)
        morph = cv2.erode( morph, kernel, iterations=3)

    # Find the contours
    image, contours, hierarchy = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # For each contour, find the bounding rectangle and draw it
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contour_area = cv2.contourArea(contour)
        rect_area = w * h
        if (contour_area / rect_area > area_ratio_thresh) and w > char_min_pxl and h > char_min_pxl:
            boxes.append([x,y,x+w,y+h])

    boxes_img = []
    if debug_:
        boxes_img = draw_boxes_on_img(np.copy(img), boxes, color=RED, thickness=4)
        imshow(morph)
        imshow(boxes_img)

    return boxes, boxes_img


def check_bw_image(image, black_thresh=16, white_thresh=240):
    black = sum(sum(image < black_thresh))
    white = sum(sum(image > white_thresh))

    pxl_sum = 0
    if len(black) == 3:
        if not black[0] == black[1] == black[2]:
            return False
        pxl_sum += black[0]
    if len(white) == 3:
        if not white[0] == white[1] == white[2]:
            return False
        pxl_sum += white[0]

    sz = image.shape
    num_pxl = sz[0] * sz[1]
    if num_pxl == pxl_sum:
        return True
    else:
        return False


def crop_images(path_in, path_out, num_images):
    filename = os.path.splitext(os.path.basename(path_in))[0]

    img = cv2.imread(path_in,0)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.split(img2)
    print(img.shape)
    print(img)
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:num_images]
    mask = np.zeros_like(img)
    i = 0
    for cnt in cnts:
        i += 1
        print(cnt.shape)
        mask = np.zeros_like(img)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
        cv2.drawContours(mask, [approx], -1, (255, 0, 0), -1)

        x,y,w,h = cv2.boundingRect(cnt)
        print(x, y, w, h)

        mask[y:y+h, x:x+w] = 255
        cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),2)

        out = np.zeros_like(img)
        out[mask == 255] = img[mask == 255]

        (x, y, _) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        out = out[topx:bottomx + 1, topy:bottomy + 1]

        img_name = filename + str(i) + '.jpeg'
        cv2.imwrite(os.path.join(path_out, img_name), out)

        # print(filename + ': ' + str(i))

    cv2.imwrite(path_out, mask)


class ContourInfo:

    def __init__(self):
        self.contours = []
        self.areas = []
        self.rect_areas = []
        self.rect_area_dims = []
        self.cxs = []
        self.cys = []

    # ------------------------------------------------------------------------------------------------------------------
    def calc_all(self):
        self.areas = []
        self.rect_areas = []
        self.rect_area_dims = []
        self.cxs = []
        self.cys = []
        for k in range(len(self.contours)):
            self.areas.append(int(cv2.contourArea(self.contours[k])))
            _, _, w, h = cv2.boundingRect(self.contours[k])
            self.rect_area_dims.append([w, h])
            self.rect_areas.append(int(w * h))
            mom = cv2.moments(self.contours[k])
            self.cxs.append(int(mom['m10']/mom['m00']) if mom['m00'] != 0 else -1)
            self.cys.append(int(mom['m01']/mom['m00']) if mom['m00'] != 0 else -1)

    # ------------------------------------------------------------------------------------------------------------------
    def contour_sorting_by_area(self, reverse=False):
        s_idx = [i[0] for i in sorted(enumerate(self.areas), key=lambda x:x[1], reverse=reverse)]
        contours = deepcopy(self.contours)
        areas = deepcopy(self.areas)
        rect_areas = deepcopy(self.rect_areas)
        cxs = deepcopy(self.cxs)
        cys = deepcopy(self.cys)
        for k in range(len(self.areas)):
            self.contours[k] = contours[s_idx[k]]
            self.areas[k] = areas[s_idx[k]]
            self.rect_areas[k] = rect_areas[s_idx[k]]
            self.cxs[k] = cxs[s_idx[k]]
            self.cys[k] = cys[s_idx[k]]

    # ------------------------------------------------------------------------------------------------------------------
    def delete_contour_info(self, idx):
        del self.contours[idx]
        del self.areas[idx]
        del self.rect_areas[idx]
        del self.rect_area_dims[idx]
        del self.cxs[idx]
        del self.cys[idx]

    # ------------------------------------------------------------------------------------------------------------------
    def check_inclusion(self, canvas, idx_small, idx_big, disp=False):
        dim = canvas.shape
        canvas = np.zeros((dim[0], dim[1], 3), dtype=np.uint8)
        cv2.drawContours(canvas, self.contours, idx_big, WHITE, -1)
        if disp:
            canvas2 = np.zeros((dim[0]+4, dim[1]+4, 3), dtype=np.uint8)
            cv2.drawContours(canvas2, self.contours, idx_big, WHITE, 1)
            cv2.drawContours(canvas2, self.contours, idx_small, RED, 1)
            for k in range(len(self.contours[idx_small])):
                pos = self.contours[idx_small][k][0]
                canvas2[pos[1]][pos[0]] = BLUE
            imshow(canvas2)

        for k in range(len(self.contours[idx_small])):
            pos = self.contours[idx_small][k][0]
            if sum(canvas[pos[1],pos[0]]) != 0:
                return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def delete_contour_from_inclusion_rule(self, img, disp=False):
        i = 0
        while i < len(self.contours) - 1:
            if self.check_inclusion(img, i+1,i, disp=disp):
                self.delete_contour_info(i)
            else:
                i += 1
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def delete_contour_from_area_rule(self, thresh=10):
        i = 0
        while i < len(self.contours):
            if self.areas[i] < thresh:
                self.delete_contour_info(i)
            else:
                i += 1

    # ------------------------------------------------------------------------------------------------------------------
    def delete_contour_from_shape_rule(self, mult=5):
        i = 0
        while i < len(self.contours):
            if self.areas[i]  * mult < self.rect_areas[i]:
                self.delete_contour_info(i)
            else:
                i += 1

    # ------------------------------------------------------------------------------------------------------------------
    def delete_contour_from_value_rule(self, img, thresh=128, disp=False):
        i = 0
        while i < len(self.contours):
            dim = img.shape
            canvas = np.zeros((dim[0], dim[1]), dtype=np.uint8)
            cv2.drawContours(canvas, self.contours, i, 255, -1)
            val = 0
            cnt = 0
            if disp:
                imshow(canvas)
            for ky in range(dim[0]):
                for kx in range(dim[1]):
                    if canvas[ky,kx] == 255:
                        val += img[ky,kx]
                        cnt += 1
            if (val / float(cnt)) < thresh:
                self.delete_contour_info(i)
            else:
                i += 1


def get_full_zoom_factor(img, zoom=0.0, factor=4/5., width=screen_width, height=screen_height):

    if isinstance(img, str):
        img = imread(img)

    dim = img.shape
    h, w = dim[0], dim[1]
    zoom_w = width  / float(w) * factor
    zoom_h = height / float(h) * factor

    if zoom == 0:
        zoom = min(zoom_h, zoom_w)
    elif zoom < 0:
        if (width < w) or (height < h):
            zoom = min(zoom_h, zoom_w)
        else:
            zoom = 1
    else:
        zoom = 1

    return zoom


def destroy_window(desc):
    cv2.waitKey(1)
    cv2.destroyWindow(desc)
    for k in range(10):
        cv2.waitKey(1)


def imresize_full(img, width=screen_width, height=screen_height):

    dim = img.shape
    h, w = dim[0], dim[1]
    if h <= 0 or w <= 0:
        zoom_w, zoom_h = 1, 1
    else:
        zoom_w = width  / float(w) * 9/10.
        zoom_h = height / float(h) * 9/10.
    zoom = min(zoom_h, zoom_w)
    return cv2.resize(img, (0,0), fx=zoom, fy=zoom), zoom


def get_video_stream_info(video_stream):
    fps = video_stream.get(cv2.CAP_PROP_FPS)
    width = int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_num = int(video_stream.get(cv2.CAP_PROP_FRAME_COUNT))
    return fps, width, height, frame_num


def read_frame(video_stream):

    flag, img_full = video_stream.read()
    if not flag:
        print(" @ Error: cannot read input video stream")
        return None
    return img_full


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def my_pause():
    print("")
    input("Press Enter to continue...")


class LocalBreak(Exception):

    def __init(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def find_common_area(px1, py1, px2, py2, qx1, qy1, qx2, qy2):

    area1 = (px2 - px1) * (py2 - py1)
    area2 = (qx2 - qx1) * (qy2 - qy1)

    if px2 < qx1 or qx2 < px1 or py2 < qy1 or qy2 < py1:
        vertex_pts = (0,0,0,0)
    else:
        vertex_pts = (max(px1, qx1), max(py1, qy1), min(px2, qx2), min(py2, qy2))
    '''
    elif px1 < qx1 < px2 < qx2 and py1 < qy1 < py2 < qy2: vertex_pts = (qx1, qy1, px2, py2)
    elif px1 < qx1 < px2 < qx2 and qy1 < py1 < qy2 < py2: vertex_pts = (qx1, py1, px2, qy2)
    elif qx1 < px1 < qx2 < px2 and py1 < qy1 < py2 < qy2: vertex_pts = (px1, qy1, qx2, py2)
    elif qx1 < px1 < qx2 < px2 and qy1 < py1 < qy2 < py2: vertex_pts = (px1, py1, qx2, qy2)

    elif px1 < qx1 < qx2 < px2 and py1 < qy1 < py2 < qy2: vertex_pts = (qx1, qy1, qx2, py2)
    elif qx1 < px1 < px2 < qx2 and qy1 < py1 < qy2 < py2: vertex_pts = (px1, py1, px2, qy2)
    elif qx1 < px1 < qx2 < px2 and py1 < qy1 < qy2 < py2: vertex_pts = (px1, qy1, qx2, qy2)
    elif px1 < qx1 < px2 < qx2 and qy1 < py1 < py2 < qy2: vertex_pts = (qx1, py1, px2, py2)
    elif px1 < qx1 < qx2 < px2 and qy1 < py1 < qy2 < py2: vertex_pts = (qx1, py1, qx2, qy2)
    elif qx1 < px1 < px2 < qx2 and py1 < qy1 < py2 < qy2: vertex_pts = (px1, qy1, px2, py2)
    elif px1 < qx1 < px2 < qx2 and py1 < qy1 < qy2 < py2: vertex_pts = (qx1, qy1, px2, qy2)
    elif qx1 < px1 < qx2 < px2 and qy1 < py1 < py2 < qy2: vertex_pts = (px1, py1, qx2, py2)

    elif px1 < qx1 < qx2 < px2 and py1 < qy1 < qy2 < py2: vertex_pts = (qx1, qy1, qx2, qy2)
    elif qx1 < px1 < px2 < qx2 and qy1 < py1 < py2 < qy2: vertex_pts = (px1, py1, px2, py2)
    '''
    area3 = (vertex_pts[1] - vertex_pts[0]) * (vertex_pts[3] - vertex_pts[2])
    ratio1 = 0. if area3 == 0 else area3 / float(area1)
    ratio2 = 0. if area3 == 0 else area3 / float(area2)

    return vertex_pts, ratio1, ratio2


def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1


def add_prefix_to_all_files(folder, prefix):
    filenames = os.listdir(folder)
    for filename  in filenames:
        if filename.split('.')[0] != "yt":
            os.rename(folder + "/" + filename, folder + "/" + prefix + filename)


def check_image_file(filename):
    ext = filename.split('.')[-1]
    if ext in ['jpg', 'png', 'bmp', 'gif', 'tiff']:
        return True
    else:
        return False


def filter_image_file_from_list(img_list):
    out_img_list = []
    for idx in range(len(img_list)):
        if check_image_file(img_list[idx]):
            out_img_list.append(img_list[idx])
    return out_img_list


def overlay_boxes_on_image(img, boxes, color, desc="", display=True):

    if boxes.ndim == 1:
        cv2.rectangle(img, (boxes[0], boxes[1]), (boxes[0] + boxes[2], boxes[1] + boxes[3]), color, 2)
    else:
        for (x, y, w, h) in boxes:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

    if display:
        imshow(img, desc=desc, zoom=0)

    return img


def image_thresholding(img, blur=5, method='BINARY'):

    img = imread(img)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if blur != 0:
        img = cv2.medianBlur(img, blur)

    if method == 'BINARY':
        ret, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    elif method == 'BINARY_INV':
        ret, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    elif method == 'TRUNC':
        ret, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
    elif method == 'TOZERO':
        ret, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
    elif method == 'TOZERO_INV':
        ret, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
    elif method == 'ADAPTIVE_MEAN':
        thresh_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    elif method == 'ADAPTIVE_GAUSSIAN':
        thresh_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    elif method == 'OTZU':
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        ret3, thresh_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        thresh_img = img
        pass

    return thresh_img


def smooth(x,window_len=11,window='hanning'):
    """
    smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the beginning and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t = linspace(-2,2,0.1)
    x = sin(t) + randn(len(t))*0.1
    y = smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)]
    instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]

    if window == 'flat':    # moving average
        w = np.ones(window_len,'d')
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(),s,mode='valid')

    return y


def modify_rect_size(rectangle, x, y):
    rect = deepcopy(rectangle)
    rect[0] = 0     if rect[0] <  0 else rect[0]
    rect[0] = x - 1 if rect[0] >= x else rect[0]
    rect[1] = 0     if rect[1] < 0  else rect[1]
    rect[1] = y - 1 if rect[1] >= y else rect[1]
    rect[2] = 0     if rect[2] <  0 else rect[2]
    rect[2] = x - 1 if rect[2] >= x else rect[2]
    rect[3] = y - 1 if rect[3] >= y else rect[3]
    rect[3] = y - 1 if rect[3] >= y else rect[3]
    return rect


'''
    if False:   # Binary image test
        methods = ['BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV', 'ADAPTIVE_MEAN', 'ADAPTIVE_GAUSSIAN',
                   'OTZU', 'NONE']
        for method in methods:
            ref_img = me.image_thresholding(arg.ref_img_file, blur=0, method=method)
            imshow(ref_img, desc=method, zoom=1.0)
'''


def add_box_overlay(img, box, color, alpha):
    """
    Add overlay box to image.

    :param img:
    :param box:
    :param color:
    :param alpha:
    :return:
    """
    # noinspection PyUnresolvedReferences
    over = cv2.rectangle(img.copy(), tuple(box[0:2]), tuple(box[2:]), color, -1)
    # noinspection PyUnresolvedReferences
    over = cv2.addWeighted(img.copy(), alpha, over, 1 - alpha, 0)
    return over


"""
def convert_to_korean_syllables(string):
    if isinstance(string, str):
        utf_str = unicode(string, 'utf-8')
"""


def get_color_histogram(img_file, color_fmt='RGB'):

    img = imread(img_file)

    if color_fmt.lower() == 'gray':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0,256])
        plt.show(hist, "Grayscale histogram", "Bins", "# of pixels", [0, 256], None)
    elif color_fmt.lower() == 'rgb':
        channels = cv2.split(img)
        colors = ('b', 'g', 'r')
        features = []
        plt.figure()
        plt.title("Flattened color histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of pixels")

        for (channel, color) in zip(channels, colors):
            hist = cv2.calcHist([channel], [0], None, [256], [0, 256])
            features.extend(hist)

            plt.plot(hist, color=color)
            plt.xlim([0, 256])

        print("flattened feature vector size : %d" % np.array(features).flatten().shape)
        plt.show()


def plt_imshow(data_2d, title=None, x_label=None, y_label=None, x_range=None, y_range=None, xticks=None, yticks=None,
               maximize_=True):
    """Show image via matplotlib.pyplot.

    :param data_2d:
    :param title:
    :param x_label:
    :param y_label:
    :param x_range:
    :param y_range:
    :param xticks:
    :param yticks:
    :param maximize_:
    :return:
    """
    if maximize_:
        if os.name == "nt":     # If Windows OS.
            plt.get_current_fig_manager().window.state('zoomed')
        else:
            plt.get_current_fig_manager().window.showMaximized()

    dim = data_2d.shape
    if len(dim) == 2:
        plt.imshow(data_2d, cmap='gray')
    elif len(dim) == 3:
        if dim[2] == 1:
            plt.imshow(data_2d, cmap='gray')
        else:
            plt.imshow(data_2d)

    if title:
        plt.title(title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    if x_range:
        plt.xlim(x_range)
    if y_range:
        plt.ylim(y_range)
    plt.xticks(xticks), plt.yticks(yticks)
    plt.show(block=True)


def plt_imshow2(img1, img2, horizontal_=True, title=(None, None), block=True):

    fig = plt.figure()

    fig.add_subplot(1,2,1) if horizontal_ else fig.add_subplot(2,1,1)
    plt.imshow(img1)
    if title[0]:
        plt.title(title)
    plt.xticks([]), plt.yticks([])

    fig.add_subplot(1,2,2) if horizontal_ else fig.add_subplot(2,1,2)
    plt.imshow(img2)
    if title[1]:
        plt.title(title)
    plt.xticks([]), plt.yticks([])
    plt.get_current_fig_manager().window.showMaximized()

    if block == 'True':
        plt.show(block=True)
    elif isinstance(block, int):
        plt.show(block=True)
        time.sleep(block)
        plt.close()


def compare_threshold_algorithms(img_gray):

    bw_imgs = [img_gray, cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
               cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2),
               cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)]

    titles = ['Original image',
              'Global thresholding (v = 127)',
              'Adaptive mean thresholding',
              'Adaptive gaussian thresholding']

    for idx in range(len(bw_imgs)):
        plt.subplot(2, 2, idx + 1), plt.imshow(bw_imgs[idx], 'gray')
        plt.title(titles[idx])
        plt.xticks([]), plt.yticks([])

    plt.show()
    pass


def derotate_img(img, compare_imgs=0, line_img_file=None, rot_img_file=None, check_time_=False):
    """Derotate image.

    :param img:
    :param compare_imgs:
    :param line_img_file:
    :param rot_img_file:
    :param check_time_:
    :return:
    """
    start_time = time.time()
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = np.amin(img, axis=2)

    check_lines_in_img_ = True
    if check_lines_in_img_:    # Test & check purpose...
        # mu.compare_threshold_algorithms(img_gray)
        _, img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        check_lines_in_img(img_bw)
        return

    _, img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    edges = cv2.Canny(img_bw, 50, 150, apertureSize=3)
    plt_imshow(edges)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

    min_idx = lines[0][:,1].argmin()
    min_angle = (90 - lines[0][min_idx,1] * 180 / np.pi)
    min_angle = int(np.sign(min_angle) * (abs(min_angle) + 0.5))

    lines_img = None
    if compare_imgs != 0 or line_img_file:
        line_img = img.copy()
        rho, theta = lines[0][min_idx]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        dim = img_bw.shape
        x1 = int(x0 - x0 * b)
        y1 = int(y0 + x0 * a)
        x2 = int(x0 + (dim[1] - x0) * b)
        y2 = int(y0 - (dim[1] - x0) * a)
        cv2.line(line_img, (x1, y1), (x2, y2), RED, 10)
        lines_img = cv2.line(lines_img, (x1, y1), (x2, y2), RED, 10)
        if line_img_file:
            imwrite(line_img_file, line_img, 'RGB')

    rot_img = imutils.rotate(img, -min_angle, (0,0), 1)
    if check_time_:
        print(" ! Time for rotation detection and doc de-rotation if any : {:.2f} sec".
              format(float(time.time() - start_time)))

    if compare_imgs != 0:
        # print(" ! angle = {:d} <- {:f}".format(min_angle, theta*180/np.pi))
        print(" ! angle = {:d}".format(min_angle))
        # plt_imshow(np.concatenate((line_img, rot_img), axis=1), title="Comparison of original and de-rotated images")
        imshow(np.concatenate((lines_img, rot_img), axis=1), pause_sec=compare_imgs)

    if rot_img_file:
        imwrite(rot_img_file, rot_img, 'RGB')

    return rot_img


# ------------------------------------------------------------------------------------------------------------------------------

def compare_strings(string1, string2, no_match_c='*', match_c='|'):
    if len(string2) < len(string1):
        string1, string2 = string2, string1
    result = ''
    n_diff = 0
    # noinspection UnresolvedReferences
    # for c1, c2 in itertools.izip(string1, string2):
    for c1, c2 in zip(string1, string2):
        if c1 == c2:
            result += match_c
        else:
            result += no_match_c
            n_diff += 1
    delta = len(string2) - len(string1)
    result += delta * no_match_c
    n_diff += delta
    return result, n_diff


def template_matching(tar_full_img,
                      tmp_full_img,
                      tar_area=None,
                      tmp_area=None,
                      method=cv2.TM_CCOEFF,
                      pause=-1):
    """
    Template matching algorithm based on opencv.

    :param tar_full_img:
    :param tmp_full_img:
    :param tar_area:
    :param tmp_area:
    :param method:
    :param pause:
    :return:
    """

    # methods
    # cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED

    if tar_area:
        dim = tar_full_img.shape
        tar_area[0] = 0      if tar_area[0] < 0      else tar_area[0]
        tar_area[1] = 0      if tar_area[1] < 0      else tar_area[1]
        tar_area[2] = dim[1] if tar_area[2] > dim[1] else tar_area[2]
        tar_area[3] = dim[0] if tar_area[3] > dim[0] else tar_area[3]
        tar_img = tar_full_img[tar_area[1]:tar_area[3],tar_area[0]:tar_area[2]]
    else:
        tar_img = tar_full_img

    if tmp_area:
        dim = tmp_full_img.shape
        tmp_area[0] = 0      if tmp_area[0] < 0      else tmp_area[0]
        tmp_area[1] = 0      if tmp_area[1] < 0      else tmp_area[1]
        tmp_area[2] = dim[1] if tmp_area[2] > dim[1] else tmp_area[2]
        tmp_area[3] = dim[0] if tmp_area[3] > dim[0] else tmp_area[3]
        tmp_img = tmp_full_img[tmp_area[1]:tmp_area[3],tmp_area[0]:tmp_area[2]]
    else:
        tmp_img = tmp_full_img

    # noinspection PyUnreachableCode
    if False:
        dim_tar = tar_img.shape
        dim_tmp = tmp_img.shape
        disp_img = np.zeros((dim_tar[0] * 2, dim_tar[1]), dtype=np.uint8)
        disp_img[:dim_tar[0], :dim_tar[1]] = tar_img
        disp_img[dim_tar[0]+8:dim_tar[0]+dim_tmp[0]+8, 8:dim_tmp[1]+8] = tmp_img
        imshow(disp_img)

    res = cv2.matchTemplate(tar_img, tmp_img, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    if pause >= 0:
        bar_num = 16
        dim = tmp_img.shape
        bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
        tar_box_img = cv2.rectangle(cv2.cvtColor(tar_img.copy(), cv2.COLOR_GRAY2RGB),
                                    top_left, bottom_right, RED, 4)
        dim_tmp = tmp_img.shape
        dim_tar = tar_box_img.shape
        merge_img = np.zeros((dim_tmp[0]+dim_tar[0]+bar_num, dim_tar[1], dim_tar[2]), dtype=np.uint8)
        merge_img[:dim_tmp[0]:,:dim_tmp[1],0] = tmp_img[:,:]
        merge_img[:dim_tmp[0]:,:dim_tmp[1],1] = tmp_img[:,:]
        merge_img[:dim_tmp[0]:,:dim_tmp[1],2] = tmp_img[:,:]
        merge_img[dim_tmp[0]+bar_num:,:,:] = tar_box_img[:,:,:]
        imshow(merge_img, desc='template matching', pause_sec=pause, loc=(10,10))

    # print(" # min_val = {:d} & max_val = {:d}".format(int(min_val), int(max_val)))

    top_left_rel = deepcopy(top_left)

    if tar_area:
        top_left = (top_left[0] + tar_area[0], top_left[1] + tar_area[1])

    return top_left, top_left_rel, min_val, max_val


# ==============================================================================================================================

def raw_input_safe(in_str):
    try:
        import termios
        time.sleep(1)
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    except all:
        pass
    return input(in_str)


def find_box_from_outside(img, pxl_val=1, thresh_ratio=0.1, disp_=False):
    """
    Find rectangle box including something from the outside of BW image.

    :param img:
    :param pxl_val:
    :param thresh_ratio:
    :param disp_:
    :return box:
    """

    dim = img.shape
    box = [-1,] * 4
    thresh = min(dim[0], dim[1]) * thresh_ratio
    margin = 2

    for idx in range(dim[1]):
        if sum(img[:,idx] < pxl_val) > thresh:
            box[0] = max(0, idx - margin)
            break

    for idx in range(dim[0]):
        if sum(img[idx,:] < pxl_val) > thresh:
            box[1] = max(0, idx - margin)
            break

    for idx in range(dim[1]-1, -1, -1):
        if sum(img[:,idx] < pxl_val) > thresh:
            box[2] = min(dim[1], idx)
            break

    for idx in range(dim[0]-1, -1, -1):
        if sum(img[idx,:] < pxl_val) > thresh:
            box[3] = min(dim[0], idx)
            break

    if disp_:
        if len(img.shape) == 2:
            disp_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            disp_img = img.copy()
        cv2.rectangle(disp_img, tuple(box[:2]), tuple(box[2:]), RED, 4)
        imshow(disp_img)

    return box


def crop_box_from_img(img, box, margin=0):
    return img[box[1]-margin:box[3]+margin, box[0]-margin:box[2]+margin]


def draw_box(img, box, color=RED, thickness=1):
    return cv2.rectangle(img, tuple(box[:2]), tuple(box[2:]), color=color, thickness=thickness)


def box_dim(box):
    return box[2] - box[0], box[3] - box[1]


def check_box_in_img_dim(box, dim):
    """

    :param box:
    :param dim:
    :return:
    """

    box[0] = 0          if box[0] <  0      else box[0]
    box[2] = dim[0] - 1 if box[2] >= dim[0] else box[2]
    box[1] = 0          if box[1] <  0      else box[1]
    box[3] = dim[1] - 1 if box[3] >= dim[1] else box[3]

    return box


"""
    # ------------------------------------------------------------------------------------------------------------------
    def hough_detection(self, check_roi):

        gray = self.tar_img[check_roi[1]:check_roi[3], check_roi[0]:check_roi[2]]
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * -b)
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 - 1000 * -b)
            y2 = int(y0 - 1000 * a)

            cv2.line(gray, (x1, y1), (x2, y2), mu.RED, 2)

        imshow(gray)

"""

##########

''''''


def is_string_nothing(string):
    if string == '' or string is None:
        return True
    else:
        return False


def is_json(my_json):
    try:
        json.loads(my_json)
        return True
    except ValueError:
        return False


def draw_line_by_equation(img, slope, sect, color=RED, thickness=3):
    """
    Draw line by equation.

    :param img:
    :param slope:
    :param sect:
    :param color:
    :param thickness:
    :return:
    """
    dim = img.shape
    pts = []
    if slope == np.inf:
        pts.append([int(sect), 0])
        pts.append([int(sect), dim[0] - 1])
    if slope == 0:
        pts.append([0, int(sect)])
        pts.append([dim[1] - 1, int(sect)])
    else:
        top_sect = int(- sect / slope)
        bot_sect = int(dim[0] - sect / slope)
        left_sect = int(sect)
        right_sect = int(slope * dim[1] + sect)
        if 0 < top_sect < dim[1]:
            pts.append([top_sect, 0])
        if 0 < bot_sect < dim[1]:
            pts.append([bot_sect, dim[1] - 1])
        if 0 < left_sect < dim[0]:
            pts.append([0, left_sect])
        if 0 < right_sect < dim[0]:
            pts.append([dim[0] - 1, right_sect])
        if len(pts) != 2:
            print(" @ Error : pts length is not 2")
            sys.exit()

    img = cv2.line(img, tuple(pts[0]), tuple(pts[1]), color=color, thickness=thickness)

    return img


def draw_box_on_img(img, box, color=RED, thickness=2, alpha=0.5):
    """
    Draw a box overlay to image.
    box format is either 2 or 4 vertex points.

    :param img:
    :param box:
    :param color:
    :param thickness:
    :param alpha:
    :return:
    """
    if np.array(box).size == 8:
        box = [box[0][0], box[0][1], box[3][0], box[3][1]]
    box = [int(x) for x in box]

    box_img = cv2.rectangle(deepcopy(img), tuple(box[0:2]), tuple(box[2:]), color, thickness)
    box_img = cv2.addWeighted(img, alpha, box_img, 1 - alpha, 0)
    return box_img


def draw_boxes_on_img(img,
                      boxes,
                      color=RED,
                      thickness=2,
                      alpha=0.,
                      margin=0,
                      add_cross_=False):
    """
    Draw the overlay of boxes to an image.
    box format is either 2 or 4 vertex points.

    :param img:
    :param boxes:
    :param color: color vector such as (R,G,B) or (R,G,B,alpha) or string 'random'
    :param thickness:
    :param alpha:
    :param margin:
    :param add_cross_:
    :return:
    """
    margins = [x * margin for x in [-1, -1, 1, 1]]

    if isinstance(color, str):
        if color.lower() == 'random':
            box_color = -1
        else:
            box_color = RED
        box_alpha = alpha
    else:
        if len(color) == 4:
            box_color = color[:3]
            box_alpha = color[3]
        else:
            box_color = color
            box_alpha = alpha

    box_img = np.copy(img)
    for cnt, box in enumerate(boxes):
        if np.array(box).size == 8:
            box = [box[0][0], box[0][1], box[3][0], box[3][1]]
        if box_color == -1:
            rand_num = random.randint(0, len(COLOR_ARRAY_RGBCMY) - 1)
            mod_color = COLOR_ARRAY_RGBCMY[rand_num]
        else:
            mod_color = box_color
        mod_box = list(map(operator.add, box, margins))
        box_img = cv2.rectangle(box_img, tuple(mod_box[0:2]), tuple(mod_box[2:]), mod_color, thickness)
        if add_cross_:
            box_img = cv2.line(box_img, (mod_box[0], mod_box[1]), (mod_box[2], mod_box[3]), color=BLACK, thickness=8)
            box_img = cv2.line(box_img, (mod_box[2], mod_box[1]), (mod_box[0], mod_box[3]), color=BLACK, thickness=8)
    disp_img = cv2.addWeighted(np.copy(img), box_alpha, box_img, 1 - box_alpha, 0)

    return disp_img


def draw_quadrilateral_on_image(img, quad_arr, color=RED, thickness=2):
    """
    Draw a quadrilateral on image.
    This function includes the regularization of quadrilateral vertices.

    :param img:
    :param quad_arr:
    :param color:
    :param thickness:
    :return:
    """
    disp_img = np.copy(img)
    if not quad_arr:
        return disp_img
    if len(np.array(quad_arr).shape) != 3:
        quad_arr = [quad_arr]

    for quad in quad_arr:
        mod_quad = np.array(regularize_quadrilateral_vertices(quad), dtype=np.int32)

        disp_img = cv2.line(disp_img, tuple(mod_quad[0]), tuple(mod_quad[1]), color=color, thickness=thickness)
        disp_img = cv2.line(disp_img, tuple(mod_quad[0]), tuple(mod_quad[2]), color=color, thickness=thickness)
        disp_img = cv2.line(disp_img, tuple(mod_quad[3]), tuple(mod_quad[1]), color=color, thickness=thickness)
        disp_img = cv2.line(disp_img, tuple(mod_quad[3]), tuple(mod_quad[2]), color=color, thickness=thickness)

    return disp_img


def generate_four_vertices_from_ref_vertex(ref, img_sz):
    """
    Generate four vertices from top-left reference vertex.

    :param ref:
    :param img_sz:
    :return:
    """

    pt_tl = [int(img_sz[0] * ref[0]), int(img_sz[1] * ref[1])]
    # pt_tr = [int(img_sz[0]), pt_tl[1]]
    pt_tr = [int(img_sz[0] - pt_tl[0]), pt_tl[1]]
    pt_bl = [pt_tl[0], int(img_sz[1] - pt_tl[1])]
    pt_br = [pt_tr[0], pt_bl[1]]

    return [pt_tl, pt_tr, pt_bl, pt_br]


def crop_image_from_ref_vertex(img, ref_vertex, symm_crop_=True, debug_=False):
    """
    Crop input image with reference vertex.

    :param img:
    :param ref_vertex:
    :param symm_crop_:
    :param debug_:
    :return:
    """
    pts = generate_four_vertices_from_ref_vertex(ref_vertex, img.shape[1::-1])
    if symm_crop_:
        crop_img = img[pts[0][1]:pts[3][1], pts[0][0]:pts[1][0]]
    else:
        crop_img = img[pts[0][1]:pts[3][1], pts[0][0]:img.shape[1]]

    if debug_:
        imshow(draw_box_on_img(img, pts, color=RED, thickness=10, alpha=0.5), desc="original image with frame")
        imshow(crop_img, desc="cropped image")
    return crop_img


def crop_image_with_coordinates(img, crop_coordinates):
    width_point_start = int(img.shape[1] * crop_coordinates[0])
    width_point_end = int(img.shape[1] * crop_coordinates[1])
    height_point_start = int(img.shape[0] * crop_coordinates[2])
    height_point_end = int(img.shape[0] * crop_coordinates[3])
    crop_img = img[height_point_start:height_point_end, width_point_start:width_point_end]

    return crop_img


########


def normalize_bboxes(bboxes, width=0, height=0, precision=4):
    norm_bboxes = []
    shift_val = pow(10, precision)
    for bbox in bboxes:
        t0 = int(bbox[0] / width  * shift_val) / shift_val
        t1 = int(bbox[1] / height * shift_val) / shift_val
        t2 = int(bbox[2] / width  * shift_val) / shift_val
        t3 = int(bbox[3] / height * shift_val) / shift_val
        t0 = 0  if t0 < 0 else t0
        t1 = 0  if t1 < 0 else t1
        t2 = t2 if t2 < 1 else 1
        t3 = t3 if t3 < 1 else 1
        norm_bboxes.append([t0, t1, t2, t3])
    return norm_bboxes


def denormalize_bboxes(bboxes, width=0, height=0):

    if not bboxes:
        return bboxes

    if bboxes[0][2] > 1 and bboxes[0][3] > 1:
        return bboxes

    denorm_bboxes = []
    for bbox in bboxes:
        t0 = int(bbox[0] * width)
        t1 = int(bbox[1] * height)
        t2 = int(bbox[2] * width)
        t3 = int(bbox[3] * height)
        denorm_bboxes.append([t0, t1, t2, t3])
    return denorm_bboxes


def check_box_boundary(box, sz):
    box[0] = 0     if box[0] < 0     else box[0]
    box[1] = 0     if box[1] < 0     else box[1]
    box[2] = sz[0] if box[2] > sz[0] else box[2]
    box[3] = sz[1] if box[3] > sz[1] else box[3]
    return box


# The following method MUST be merged with rearrange_quad_with_type method.
def regularize_quadrilateral_vertices(vertices):
    """
    Regularize quadrilateral vertices to the de-facto rule. (LT, RT, LB, RB)

    :param vertices: 2D list of position list of (x, y)
    :return:
    """
    out = sorted(vertices, key=operator.itemgetter(0))
    if out[0][1] > out[1][1]:
        out[0], out[1] = out[1], out[0]
    if out[2][1] > out[3][1]:
        out[2], out[3] = out[3], out[2]
    out[1], out[2] = out[2], out[1]
    return out


def rearrange_quad_with_type(quad, quad_type='zigzag'):

    q0 = quad.tolist() if isinstance(quad, np.ndarray) else quad
    q1 = sorted(q0, key=lambda x: x[1], reverse=False)
    if q1[0][0] > q1[1][0]:
        q1[0], q1[1] = q1[1], q1[0]
    if q1[2][0] > q1[3][0]:
        q1[2], q1[3] = q1[3], q1[2]

    if quad_type == 'zigzag':
        pass
    elif quad_type == 'clockwise':
        q1[2], q1[3] = q1[3], q1[2]
    else:
        print(" @ Error: incorrect quad_type, {}, in rearrange_quad method.".format(quad_type))

    return q1


def crop_rect_from_quad(img, quad, perspective_=True):

    height, width, _ = img.shape
    if perspective_:
        np_quad = np.array(quad)
        crop_width  = int(((np_quad[1][0] - np_quad[0][0]) + (np_quad[3][0] - np_quad[2][0])) / 2.)
        crop_height = int(((np_quad[2][1] - np_quad[0][1]) + (np_quad[3][1] - np_quad[1][1])) / 2.)
        pts1 = np.float32(np_quad)
        pts2 = np.float32([[0,0],[crop_width,0],[0,crop_height],[crop_width,crop_height]])
        m = cv2.getPerspectiveTransform(pts1, pts2)
        trans_img = cv2.warpPerspective(img, m, (crop_width, crop_height))
        crop_img = trans_img[0:crop_height,0:crop_width]
    else:
        x_min = int(quad[0][0] if quad[0][0] < quad[2][0] else quad[2][0])
        x_max = int(quad[1][0] if quad[1][0] > quad[3][0] else quad[3][0])
        y_min = int(quad[0][1] if quad[0][1] < quad[1][1] else quad[1][1])
        y_max = int(quad[2][1] if quad[2][1] > quad[3][1] else quad[3][1])
        crop_img = img[y_min:y_max,x_min:x_max]
    return crop_img


def expand_quad_with_margin(quad, margin=0, width=None, height=None):

    ext_quad = [[quad[0][0] - margin, quad[0][1] - margin],
                [quad[1][0] + margin, quad[1][1] - margin],
                [quad[2][0] - margin, quad[2][1] + margin],
                [quad[3][0] + margin, quad[3][1] + margin]]

    if width is not None:
        ext_quad[0][0] = width[0] if ext_quad[0][0] < width[0] else ext_quad[0][0]
        ext_quad[1][0] = width[1] if ext_quad[1][0] > width[1] else ext_quad[1][0]
        ext_quad[2][0] = width[0] if ext_quad[2][0] < width[0] else ext_quad[2][0]
        ext_quad[3][0] = width[1] if ext_quad[3][0] > width[1] else ext_quad[3][0]

    if height is not None:
        ext_quad[0][0] = height[0] if ext_quad[0][1] < height[0] else ext_quad[0][0]
        ext_quad[1][0] = height[1] if ext_quad[1][1] > height[1] else ext_quad[1][0]
        ext_quad[2][0] = height[0] if ext_quad[2][1] < height[0] else ext_quad[2][0]
        ext_quad[3][0] = height[1] if ext_quad[3][1] > height[1] else ext_quad[3][0]

    if isinstance(ext_quad, np.ndarray):
        return np.array(ext_quad)
    else:
        return ext_quad


def reorder_quads(quads, axis='x'):
    quad_list = quads.tolist() if isinstance(quads, np.ndarray) else deepcopy(quads)
    if axis == 'x':
        return sorted(quad_list, key=lambda x: x[0][0], reverse=False)
    elif axis == 'y':
        return sorted(quad_list, key=lambda x: x[0][1], reverse=False)
    else:
        return quad_list


def get_random_color(color_len=3):
    if color_len == 3:
        color_arr = COLOR_ARRAY_RGB
    elif color_len == 5:
        color_arr = COLOR_ARRAY_RGBKW
    elif color_len == 6:
        color_arr = COLOR_ARRAY_RGBCMY
    elif color_len == 8:
        color_arr = COLOR_ARRAY_RGBCMYKW
    else:
        color_arr = COLOR_ARRAY_RGB
    return color_arr[random.randint(0, len(color_arr) - 1)]


def normalize_box(box, w, h):
    ww = float(w)
    hh = float(h)
    shape = np.array(box).shape
    if shape[0] == (1,4):
        out = [box[0] / ww, box[1] / hh, box[2] / ww, box[3] / hh]
    elif shape == (1,8):
        out = [box[0] / ww, box[1] / hh, box[2] / ww, box[3] / hh,
               box[4] / ww, box[5] / hh, box[6] / ww, box[7] / hh]
    elif shape[0] == 2:
        out = [[p[0]/ww, p[1]/hh] for p in box]
    else:
        print(" @ Error: box shape is not defined, {}.".format(str(shape)))
        out = box

    if isinstance(box, np.ndarray):
        return np.array(out)
    else:
        return out


def non_max_suppression_fast(boxes, overlap_thresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    # initialize the list of picked indexes
    pick = []
    # grab the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    # keep looping while some indexes still remain in the indexes list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))
    # return only the bounding boxes that were picked using the integer data type
    return boxes[pick].astype("int")


def update_bboxes_with_offset_and_scale(bboxes, offset=None, scale=None, forward_=True):
    offset = [0, 0] if offset is None else offset
    scale  = [1, 1] if scale  is None else scale

    output = []
    if forward_:
        for i, bbox in enumerate(bboxes):
            output.append([bbox[i] * scale[i % 2] + offset[i % 2] for i in range(len(bbox))])
    else:
        for i, bbox in enumerate(bboxes):
            output.append([(bbox[i] - offset[i % 2]) *  scale[i % 2] for i in range(len(bbox))])
    return output


def update_polygons_with_offset_and_scale(polygons, offset=None, scale=None, forward_=True):
    output = np.array(polygons)
    offset = np.array([0, 0] if offset is None else offset)
    scale  = np.array([1, 1] if scale  is None else scale)

    if forward_:
        for i, polygon in enumerate(polygons):
            output[i] = polygon * scale + offset
    else:
        for i, polygon in enumerate(polygons):
            output[i] = (polygon - offset) * scale
    return output


def compare_image_folders(folder1, folder2, direction='horizontal', pause_sec=0):
    filenames1 = sorted(utils.get_filenames_in_a_directory(folder1))
    for filename in filenames1:
        if os.path.splitext(filename)[1][1:] in utils.IMG_EXTENSIONS:
            print(" # Compare {}".format(filename))
            img1 = imread(os.path.join(folder1, filename))
            if os.path.isfile(os.path.join(folder2, filename)):
                img2 = imread(os.path.join(folder2, filename))
            else:
                img2 = np.zeros(tuple(img1.shape), dtype=np.uint8)
            if direction == 'horizontal':
                img = hstack_images((img1, img2))
            else:
                img = vstack_images((img1, img2))
            imshow(img, desc="compare image " + os.path.basename(filename), pause_sec=pause_sec)


def cvimg2pilimg(cvimg):
    # noinspection PyUnresolvedReferences
    return Image.fromarray(cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB))


def pilimg2cvimg(pilimg):
    # noinspection PyUnresolvedReferences
    return np.asarray(cv2.cvtColor(pilimg, cv2.COLOR_RGB2BGR))


# noinspection PyPep8Naming
def put_text_twice(img, text, pos, font, scale, colors, thickness):
    # noinspection PyUnresolvedReferences
    img = cv2.putText(img, text, pos, font, scale, colors[0], thickness[0])
    # noinspection PyUnresolvedReferences
    img = cv2.putText(img, text, pos, font, scale, colors[1], thickness[1])

    return img


# noinspection PyPep8Naming
def cvLine_with_boundary(img, p0, p1, colors, thickness):
    # noinspection PyUnresolvedReferences
    img = cv2.line(img, p0, p1, colors[0], thickness[0])
    # noinspection PyUnresolvedReferences
    img = cv2.line(img, p0, p1, colors[1], thickness[1])

    return img


def get_intersection_ratio(src_bbox, tar_bbox):       # returns None if rectangles don't intersect
    dx = min(src_bbox[2], tar_bbox[2]) - max(src_bbox[0], tar_bbox[0])
    dy = min(src_bbox[3], tar_bbox[3]) - max(src_bbox[1], tar_bbox[1])
    if (dx >= 0) and (dy >= 0):
        return dx * dy / ((src_bbox[2] - src_bbox[0]) * (src_bbox[3] - src_bbox[1]))
    else:
        return 0


def get_similar_bbox(src_bbox, tar_bboxes, thresh=0.9):
    for i, tar_bbox in enumerate(tar_bboxes):
        iou_ratio = get_intersection_ratio(src_bbox, tar_bbox)
        if iou_ratio > thresh:
            return i, iou_ratio
    return None, 0


def get_interp_bboxes(src_bbox, tar_bbox, interp_num=1):

    interp_bboxes = []
    for idx in range(interp_num):
        scales = [x / (interp_num + 1) for x in [idx + 1, interp_num - idx]]

        x0 = int(src_bbox[0] * scales[1] + tar_bbox[0] * scales[0])
        y0 = int(src_bbox[1] * scales[1] + tar_bbox[1] * scales[0])
        x1 = int(src_bbox[2] * scales[1] + tar_bbox[2] * scales[0])
        y1 = int(src_bbox[3] * scales[1] + tar_bbox[3] * scales[0])

        interp_bboxes.append([x0, y0, x1, y1])

    return interp_bboxes