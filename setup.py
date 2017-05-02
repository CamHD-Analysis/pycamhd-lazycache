from setuptools import setup
import io, re, os

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

version = find_version('pycamhd', '__init__.py')

setup(name='pylazycamhd',
      version=version,
      description='Module for interacting with a LazyCache server',
      long_description='README.rst',
      url='https://github.com/CamHD-Analysis/pylazycamhd',
      author='Aaron Marburg',
      author_email='amarburg@apl.washington.edu',
      license='MIT',
      packages=['pylazycamhd'])
