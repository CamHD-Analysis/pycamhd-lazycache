#!/usr/bin/env python

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from PIL import Image
from io import BytesIO

import urllib.parse
import numpy as np
import re

import logging

# Current CamHD Cache hosted at Digital Ocean
DEFAULT_LAZYCACHE = 'https://cache.camhd.science/v1/org/oceanobservatories/rawdata/files'


DEFAULT_TIMEOUT = 10  # seconds

## Based on retry methods described at:
## https://www.peterbe.com/plog/best-practice-with-retries-with-requests

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session



def get_metadata( url, timeout = DEFAULT_TIMEOUT):
    r = requests_retry_session().get( url, timeout=timeout )

    if r.status_code != 200:
        return None

    return r.json()


## Retrieve the frame'th frame from the mirror site at url
def get_frame(orig_url, frame_num, format='np', timeout=DEFAULT_TIMEOUT, fail_raw=False, width=1920, height=1080):

    url = urllib.parse.urlsplit( orig_url )

    DIRECT_FROM_SERVER_FORMATS = ['png', 'jpg', 'jpeg', 'bmp']

    # Image size parameters as a suffix for the URL.
    if width <= 0 and width > 1920:
        raise ValueError("The width parameter is invalid: %s" % width)

    if height <= 0 and height > 1080:
        raise ValueError("The height parameter is invalid: %s" % width)

    img_size_url_suffix = "?width=%d&height=%d" % (width, height)

    ## These formats can be requested directly from the server
    fmt = ""
    if format in DIRECT_FROM_SERVER_FORMATS:
        fmt = ".%s" % format

        url = url._replace(path=url.path + "/frame/%d%s%s" % (frame_num, fmt, img_size_url_suffix))
        full_url = urllib.parse.urlunsplit(url)
        logging.info("pycamhd.lazycache: requesting %s" % full_url)

        r = requests_retry_session().get( full_url, timeout = timeout  )

        # TODO.  More validation here could be done here...
        if r.status_code != 200:
            return None

        img = Image.open( BytesIO( r.content ) )
        return img

    elif format in ['np','Image']:

        url = url._replace(path=url.path + "/frame/%d.rgba%s" % (frame_num, img_size_url_suffix))
        full_url = urllib.parse.urlunsplit(url)
        logging.info("pycamhd.lazycache: requesting %s" % full_url)

        r = requests_retry_session().get(full_url, timeout=timeout)

        # If the server can't handle rawdata,
        if r.status_code == 501:

            if fail_raw:
                # Should this be an exception?
                return None

            # Fallback to getting the PNG
            img = get_frame(orig_url, frame_num, format='png', timeout=timeout, width=width, height=height)
            if not img:
                return None

            ## The PNG comes without an alpha channel, interestingly...
            img.putalpha(1)

            if format is 'np':
                return np.array(img.convert())

            return img


        # TODO.  More validation here could be done here...
        if r.status_code != 200:
            return None

        if format is 'Image':
            img = Image.frombytes('RGBA', [width, height], r.content)
            return img


        array =  np.frombuffer(r.content, dtype=np.dtype('uint8'))
        return np.reshape(array, [height, width, 4])

    else:
        logging.error("Don't understand format type \"%s\"" % format)
        return None

## Retrieve the frame'th frame from the mirror site at url
def save_frame( url, frame_num, filename, format = 'np', timeout = DEFAULT_TIMEOUT ):

    url = urllib.parse.urlsplit( url )

    ## These  formats can be requested directly from the server
    DIRECT_FROM_SERVER_FORMATS = ['png', 'jpg', 'jpeg']

    fmt = ""
    if format in DIRECT_FROM_SERVER_FORMATS:
        fmt = ".%s" % format

    url = url._replace( path=url.path + "/frame/%d%s" % (frame_num,fmt) )

    full_url = urllib.parse.urlunsplit( url )

    #logging.info("pycamhd.lazycache: requesting %s" % full_url )

    r = requests_retry_session().get( full_url, timeout = timeout  )

    if r.status_code != 200:
        return None

    with open(filename, 'wb') as f:
        f.write(r.content)

def get_dir( url ):
    r = requests.get( url )

    if r.status_code != 200:
        return None

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

# Given just the basename (the movie filename), returns the full path in the
# CI hierarchy
def convert_basename( basename ):
    prog = re.compile("CAMHDA301-(\d{4})(\d{2})(\d{2})T\d{6}")
    match = re.match(prog, basename)

    return "/RS03ASHS/PN03B/06-CAMHDA301/%04d/%02d/%02d/%s.mov" % (int(match.group(1)), int(match.group(2)), int(match.group(3)),basename)



# An object-oriented version of the same API
class LazycacheAccessor:
    def __init__(self, lazycache=DEFAULT_LAZYCACHE, verbose=False ):
        self.lazycache = lazycache if lazycache else DEFAULT_LAZYCACHE
        self.verbose = verbose

    def merge_url( self, path ):
        # Merge path into lazycache URL
        url = urllib.parse.urlsplit(self.lazycache)
        url = url._replace(path=url.path + path)
        return urllib.parse.urlunsplit(url)

    def get_metadata(self, url, timeout = DEFAULT_TIMEOUT ):
        url = self.merge_url(url)
        if self.verbose:
            print("get_metadata: %s" % url)
        return get_metadata(url, timeout=timeout)

    def get_frame(self, url, frame_num, format='np', timeout=DEFAULT_TIMEOUT, width=1920, height=1080):
        url = self.merge_url(url)
        if self.verbose:
            print("get_frame: %s" % url)
        return get_frame( url, frame_num, format=format, timeout=timeout, width=width, height=height)

    def save_frame(self, url, frame_num, filename, format = 'np', timeout =  DEFAULT_TIMEOUT ):
        url = self.merge_url(url)
        if self.verbose:
            print("get_frame: %s" % url)
        return save_frame( url, frame_num, filename, format=format, timeout = timeout )

    def get_dir( self, url ):
        url = self.merge_url( url )
        if self.verbose:
            print("get_dir: %s" % url)
        return get_dir( url )

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



def lazycache( url=DEFAULT_LAZYCACHE, verbose=False):
    if not url:
        url = DEFAULT_LAZYCACHE

    return LazycacheAccessor(url, verbose=verbose)
