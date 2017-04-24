#!/usr/bin/env python
# This script uses the pycamhd module to print the number of frames in a remote
# video file.
#
# Aaron Marburg (amarburg@apl.washington.edu)
# Copied from Timothy Crone (tjcrone@gmail.com)

import sys, pylazycamhd

# remote file
filename = '/RS03ASHS/PN03B/06-CAMHDA301/2016/11/13/CAMHDA301-20161113T000000Z.mov'
cache_url = 'https://camhd-app-dev.appspot.com/v1/org/oceanobservatories/rawdata/files'

# download moov_atom from remote file
movie = pylazycamhd.get_movie_metadata( cache_url + filename )

if movie:
    print(movie)
    sys.stdout.write("Frame count: %i\n" % movie["NumFrames"])
