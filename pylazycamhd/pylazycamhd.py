#!/usr/bin/env python

import requests
from PIL import Image
from io import BytesIO

def get_movie_metadata( url ):
    r = requests.get( url )

    if r.status_code != 200:
        return

    return r.json()


## Retrieve the frame'th frame from the mirror site at url
def get_movie_frame( url, frame ):
    r = requests.get( (url + "/frame/%d") % frame )

    if r.status_code != 200:
        return

    # TODO.  Lots more validation here could be done here...

    return Image.open( BytesIO( r.content ) )
