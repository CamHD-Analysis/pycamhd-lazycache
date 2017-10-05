#!/usr/bin/env python

import pycamhd
import numpy as np
from PIL import Image
import random

# remote file



DEFAULT_FRAME_NUM=5000

# This file is in the overlay on Berna
filename_overlay = '/RS03ASHS/PN03B/06-CAMHDA301/2016/07/24/CAMHDA301-20160724T030000Z.mov'

# This file is _not_ in the overlay on Berna
filename_nonoverlay = '/RS03ASHS/PN03B/06-CAMHDA301/2016/11/13/CAMHDA301-20161113T000000Z.mov'

test_lazycache = 'http://localhost:8080/v1/org/oceanobservatories/rawdata/files'

def check_image(img, format=None, mode="RGBA"):

    if format is 'np':
        assert isinstance( img, np.ndarray )

        shape = img.shape
        assert shape[2] == 4   # RGBA?
        assert shape[1] == 1920
        assert shape[0] == 1080
        return

    ## For other formats, the object should be a PIL.Image.Image
    ## PIL only knows "JPEG", not 'JPG'
    format = "jpeg" if format == 'jpg' else format

    assert isinstance( img, Image.Image )

    assert img.width == 1920
    assert img.height == 1080

    if mode and format is "Image":
        assert img.mode == mode
    else:
        if format:
            assert img.format == format.upper()


def do_get_frame(filename, format):
    ## TODO:   This mechanism results in downloading the same frame_num repeatedly...
    ## Fix so it's actually downloading different images
    meta=pycamhd.Lazycache.get_metadata(test_lazycache+filename)
    img=pycamhd.Lazycache.get_frame(test_lazycache + filename, frame_num=random.uniform(0,meta['NumFrames']), format=format)
    check_image(img,format)


## Could I generate these programmatically?

def test_get_frame_np_overlay():
    do_get_frame(filename_overlay, "np")

def test_get_frame_np_nonoverlay():
    do_get_frame(filename_nonoverlay, "np")

def test_get_frame_PIL_Image_overlay():
    do_get_frame(filename_overlay, "Image")

def test_get_frame_PIL_Image_nonoverlay():
    do_get_frame(filename_nonoverlay, "Image")

def test_get_frame_bmp_overlay():
    do_get_frame(filename_overlay, "bmp")

def test_get_frame_bmp_nonoverlay():
    do_get_frame(filename_nonoverlay, "bmp")

def test_get_frame_jpg_overlay():
    do_get_frame(filename_overlay, "jpg")

def test_get_frame_jpg_nonoverlay():
    do_get_frame(filename_nonoverlay, "jpg")

def test_get_frame_png_overlay():
    do_get_frame(filename_overlay, "png")

def test_get_frame_png_nonoverlay():
    do_get_frame(filename_nonoverlay, "png")
