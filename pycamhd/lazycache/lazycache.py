#!/usr/bin/env python

import requests
from PIL import Image
from io import BytesIO

import urllib.parse
import numpy as np

def get_metadata( url ):
    r = requests.get( url )

    if r.status_code != 200:
        return

    return r.json()


## Retrieve the frame'th frame from the mirror site at url
def get_frame( url, frame_num, format = 'np' ):
    url = urllib.parse.urlsplit( url )
    new_url = url._replace( path= url.path + "/frame/%d" % frame_num )
    full_url = urllib.parse.urlunsplit( new_url )

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
