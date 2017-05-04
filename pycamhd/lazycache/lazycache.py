#!/usr/bin/env python

import requests
from PIL import Image
from io import BytesIO

import urllib.parse
import numpy as np

DEFAULT_LAZYCACHE = 'https://camhd-app-dev.appspot.com/v1/org/oceanobservatories/rawdata/files'


def get_metadata( url, lazycache = DEFAULT_LAZYCACHE ):
    r = requests.get( url )

    if r.status_code != 200:
        return

    return r.json()


## Retrieve the frame'th frame from the mirror site at url
def get_frame( url, frame_num, format = 'np' ):
    url = urllib.parse.urlsplit( url )
    url = url._replace( path= url.path + "/frame/%d" % frame_num )
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


class LazycacheAccessor:
    def __init__(self, lazycache = DEFAULT_LAZYCACHE ):
        self.lazycache = lazycache

    def merge_url( self, path ):
        ## Merge path into lazycache URL
        url = urllib.parse.urlsplit( self.lazycache )
        url = url._replace( path= url.path + path )
        return urllib.parse.urlunsplit( url )

    def get_metadata( self, url ):
        return get_metadata( self.merge_url( url ) )

    def get_frame( self, url, frame_num, format = 'np'):
        return get_frame( self.merge_url( url ), frame_num, format )

def lazycache( url  = DEFAULT_LAZYCACHE ):
    return LazycacheAccessor( url )
