#!/usr/bin/env python

import pycamhd.lazycache as camhd
import numpy as np
from PIL import Image
import random

# remote file

#filename = '/RS03ASHS/PN03B/06-CAMHDA301/2016/11/13/CAMHDA301-20161113T000000Z.mov'
DEFAULT_FRAME_NUM=5000

# this file is in the overlay...
filename = '/RS03ASHS/PN03B/06-CAMHDA301/2016/07/24/CAMHDA301-20160724T030000Z.mov'

test_lazycache = 'http://localhost:8080/v1/org/oceanobservatories/rawdata/files'

def check_image(img, format=None, mode="RGBA"):

    if format is 'np':
        assert isinstance( img, np.ndarray )

        shape = img.shape
        assert shape[2] == 4   # RGBA?
        assert shape[1] == 1920
        assert shape[0] == 1080
        return


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

def do_get_frame(format, frame_num=DEFAULT_FRAME_NUM):
    return camhd.get_frame(test_lazycache + filename, frame_num, format=format)

def test_get_frame_np(benchmark):
    meta=camhd.get_metadata(test_lazycache+filename)
    img=benchmark(do_get_frame, frame_num=random.uniform(0,meta['NumFrames']), format="np")
    check_image(img,'np')

def test_get_frame_PIL_image(benchmark):
    format="Image"
    meta=camhd.get_metadata(test_lazycache+filename)
    img=benchmark(do_get_frame,format, frame_num=random.uniform(0,meta['NumFrames']))
    check_image(img,format)

def test_get_frame_png(benchmark):
    format="png"
    meta=camhd.get_metadata(test_lazycache+filename)
    img=benchmark(do_get_frame, format, frame_num=random.uniform(0,meta['NumFrames']))
    check_image(img,format)

def test_get_frame_jpg(benchmark):
    format="jpg"
    meta=camhd.get_metadata(test_lazycache+filename)
    img=benchmark(do_get_frame, format, frame_num=random.uniform(0,meta['NumFrames']))
    check_image(img,format)

def test_get_frame_bmp(benchmark):
    format="bmp"
    meta=camhd.get_metadata(test_lazycache+filename)
    img=benchmark(do_get_frame, format, frame_num=random.uniform(0,meta['NumFrames']))
    check_image(img,format)





## Test file can be run as a standalone.  Why?  Was diagnosing segfaults
# and some of the debug output was being hidden by pytest
if __name__ == "__main__":
    test_get_frame_image()
