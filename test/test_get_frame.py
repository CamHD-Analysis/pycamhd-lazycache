#!/usr/bin/env python

import pycamhd.lazycache as camhd
import numpy as np
from PIL import Image

# remote file
filename = '/RS03ASHS/PN03B/06-CAMHDA301/2016/11/13/CAMHDA301-20161113T000000Z.mov'
test_lazycache = 'http://localhost:8080/v1/org/oceanobservatories/rawdata/files'


def check_image(img, format=None, mode=None):
    assert isinstance( img, Image.Image )

    assert img.width == 1920
    assert img.height == 1080

    if format:
        assert img.format == format

    if mode:
        assert img.mode == mode


def check_np(img):
    assert isinstance( img, np.ndarray )

    shape = img.shape
    assert shape[2] == 4   # RGBA?
    assert shape[1] == 1920
    assert shape[0] == 1080


def test_get_frame_np():
    # download moov_atom from remote file
    img = camhd.get_frame( test_lazycache + filename, 5000 )
    check_np(img)

def test_get_frame_PIL_image():
    # download moov_atom from remote file
    img = camhd.get_frame( test_lazycache + filename, 5000, format = "Image" )

    check_image( img, mode="RGBA")


def test_get_frame_image():

    for format in ['png', 'jpeg', 'jpg']:
        # download moov_atom from remote file
        img = camhd.get_frame( test_lazycache + filename, 5000, format = format )

        ## PIL only knows "JPEG"
        format = "jpeg" if format == 'jpg' else format

        check_image(img, format=format.upper())

## Object-oriented version
def test_get_frame_np_oo():
    r = camhd.lazycache( test_lazycache )
    img = r.get_frame( filename, 5000 )

    assert isinstance( img, np.ndarray )

    shape = img.shape
    assert shape[1] == 1920
    assert shape[0] == 1080


## Test file can be run as a standalone.  Why?  Was diagnosing segfaults
# and some of the debug output was being hidden by pytest
if __name__ == "__main__":
    test_get_frame_image()
