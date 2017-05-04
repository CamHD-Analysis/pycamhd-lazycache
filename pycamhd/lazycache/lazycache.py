#!/usr/bin/env python

import requests
from PIL import Image
from io import BytesIO

import urllib.parse
import numpy as np

DEFAULT_LAZYCACHE = 'https://camhd-app-dev.appspot.com/v1/org/oceanobservatories/rawdata/files'


def get_metadata( path, lazycache = DEFAULT_LAZYCACHE ):
    ## Merge path into lazycache URL
    url = urllib.parse.urlsplit( lazycache )
    url = url._replace( path= url.path + path )
    full_url = urllib.parse.urlunsplit( url )

    r = requests.get( full_url )

    if r.status_code != 200:
        return

    return r.json()



## Retrieve the frame'th frame from the mirror site at url
def get_frame( path, frame_num, format = 'np', lazycache = DEFAULT_LAZYCACHE ):
    url = urllib.parse.urlsplit( lazycache )
    url = url._replace( path= url.path + path + "/frame/%d" % frame_num )
    full_url = urllib.parse.urlunsplit( url )

    r = requests.get( full_url  )

    if r.status_code != 200:
        return

    # TODO.  Lots more validation here could be done here...

    if format == 'np':
        png = Image.open( BytesIO( r.content ) )
        return np.array( png.convert() )
    elif format == 'image':
        return Image.open( BytesIO( r.content ) )
    else:
        print("Don't understand format type \"%s\"" % format)
        return
