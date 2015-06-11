from setuptools import setup, find_packages
import sys

#a crude test that ensure xraylib is installed...
try:
    import xraylib
except ImportError:
    print("Could not detect xraylib-python bindings. Ensure these are installed before continuing")
    sys.exit(1)

setup(
    name = "xrmc",
    version = "6.6.0",
    py_modules = ['xrmc'],
    scripts = ['xrmc-plot', 'xrmc-plot-dscan'],

    requires = ['numpy', 'matplotlib'],
    install_requires = ['numpy', 'matplotlib'],

    author = "Tom Schoonjans",
    author_email = "Tom.Schoonjans@gmail.com",
    description = "Utilities around the XRMC package",
    license = "GPLv3",
    url = "https://github.com/tschoonj/xrmc-utils/"

)
