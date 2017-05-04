#!/usr/bin/env python

import pycamhd.lazycache as camhd
import numpy as np
from PIL import Image

# remote file
filename = '/RS03ASHS/PN03B/06-CAMHDA301/2016/11/13/CAMHDA301-20161113T000000Z.mov'

def test_get_frame_np():
    # download moov_atom from remote file
    img = camhd.get_frame( filename, 5000 )

    assert isinstance( img, np.ndarray )

    shape = img.shape
    assert shape[1] == 1920
    assert shape[0] == 1080


def test_get_frame_image():
    # download moov_atom from remote file
    img = camhd.get_frame( filename, 5000, format = 'image' )

    assert isinstance( img, Image.Image )

    shape = img.size
    assert shape[0] == 1920
    assert shape[1] == 1080
