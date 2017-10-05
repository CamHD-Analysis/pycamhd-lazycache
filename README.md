# PyLazyCamHD

Python API for accessing [CamHD](http://novae.ocean.washington.edu/story/Ashes_CAMHD_Live) data from a  [go-lazycache](https://github.com/amarburg/go-lazycache) instance.   
As we're calling the the HTTP API exposed by Lazycache, this package is 
lightweight  --- basically just a wrapper around HTTP requests.

## Test

`pytest` must be installed

   python -m pytest


## benchmark

`pytest` and `pytest-benchmark` must be installed.

   python -m pytest benchmarks/

# License

[MIT License](LICENSE) (c) 2017 Aaron Marburg
