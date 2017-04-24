#!/usr/bin/env python
# This script uses the pycamhd module to print the number of frames in a remote
# video file.
#
# Aaron Marburg (amarburg@apl.washington.edu)
# Copied from Timothy Crone (tjcrone@gmail.com)

import sys
import pylazycamhd
import numpy as np

# remote file
filename = '/RS03ASHS/PN03B/06-CAMHDA301/2016/11/13/CAMHDA301-20161113T000000Z.mov'
cache_url = 'https://camhd-app-dev.appspot.com/v1/org/oceanobservatories/rawdata/files'

# download moov_atom from remote file
img = pylazycamhd.get_movie_frame( cache_url + filename, 5000 )

arr = np.array(img.convert("L"))
print(arr.shape)
