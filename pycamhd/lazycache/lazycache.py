#!/usr/bin/env python

import requests
from PIL import Image
from io import BytesIO

import urllib.parse
import numpy as np
import re

DEFAULT_LAZYCACHE = 'https://camhd-app-dev.appspot.com/v1/org/oceanobservatories/rawdata/files'


def get_metadata( url, lazycache = DEFAULT_LAZYCACHE, timeout = 2 ):
    r = requests.get( url, timeout=timeout )

    if r.status_code != 200:
        return

    return r.json()


## Retrieve the frame'th frame from the mirror site at url
def get_frame( url, frame_num, format = 'np', timeout = 2 ):
    url = urllib.parse.urlsplit( url )
    url = url._replace( path= url.path + "/frame/%d" % frame_num )
    full_url = urllib.parse.urlunsplit( url )

    r = requests.get( full_url, timeout = timeout  )

    if r.status_code != 200:
        return

    png = Image.open( BytesIO( r.content ) )
    png.save("frame.png")

    # TODO.  Lots more validation here could be done here...
    if format == 'np':
        return np.array( png.convert() )
    elif format == 'image':
        return png
    else:
        print("Don't understand format type \"%s\"" % format)
        return

def get_dir( url ):
    print("Querying ", url)
    r = requests.get( url )
    return r.json()

def find( url, regexp = 'mov$' ):
    out = []
    dir_json = get_dir( url )
    for d in dir_json['Directories']:
        out += get_dir( url + d )

    for f in dir_json['Files']:
        if re.search( regexp, f ):
            out += f

    return out


class LazycacheAccessor:
    def __init__(self, lazycache = DEFAULT_LAZYCACHE ):
        self.lazycache = lazycache

    def merge_url( self, path ):
        ## Merge path into lazycache URL
        url = urllib.parse.urlsplit( self.lazycache )
        url = url._replace( path= url.path + path )
        return urllib.parse.urlunsplit( url )

    def get_metadata( self, url, timeout = 2 ):
        return get_metadata( self.merge_url( url ), timeout = timeout )

    def get_frame( self, url, frame_num, format = 'np', timeout = 2):
        return get_frame( self.merge_url( url ), frame_num, format=format, timeout = timeout )

    def get_dir( self, url ):
        return get_dir( self.merge_url(url) )

    ## Duplicate this functionality so that URLs remain repo-relative
    def find( self, url, regexp = 'mov$' ):
        out = []
        dir_json = self.get_dir( url )
        for d in dir_json['Directories']:
            out += self.get_dir( url + d )

        for f in dir_json['Files']:
            if re.search( regexp, f ):
                out += [url + "/" + f]

        return out



def lazycache( url  = DEFAULT_LAZYCACHE ):
    return LazycacheAccessor( url )
