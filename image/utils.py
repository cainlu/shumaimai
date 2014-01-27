#coding=utf-8

import Image
import os
from cStringIO import StringIO

from django.conf import settings

def zoom(image, width=None, height=None):
    (ori_width, ori_height) = image.size
    if width is None and height is None:
        size = (ori_width, ori_height)
    elif width is None and height is not None:
        res_width =  ori_width * height / ori_height
        size = (res_width, height)
    elif width is not None and height is None:
        res_height = ori_height * width / ori_width
        size = (width, res_height)
    else:
        size = (width, height)
    return image.resize(size, Image.ANTIALIAS)

def crop(image, width=None, height=None, left=0, top=0):
    (ori_width, ori_height) = image.size
    if width is None:
        width = ori_width
    if height is None:
        height = ori_height
    box = (left, top, width, height)
    return image.crop(box)

def process(image, mode=None, width=None, height=None):
    ''' change image according to parameters '''
    if mode is None:
        return image
    mode = int(mode)
    if mode == 1:
        return zoom(image, width=width, height=height)
    elif mode == 2:
        return crop(image, width=width, height=height)
    else:
        raise Exception("Mode is illegal.")

def image_factory(path, mode=None, width=None, height=None):
    real_path = path
    try:
        im_tmp = Image.open(real_path)
    except:
        im_tmp = Image.open(settings.DEFAULT_IMAGE_PATH)
    im_res = process(im_tmp, mode, width, height)
    return im_res




