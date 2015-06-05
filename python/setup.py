from setuptools import setup, find_packages
setup(
    name = "xrmc",
    version = "6.6.0",
    packages = find_packages(),

    install_requires = ['numpy', 'matplotlib'],

    author = "Tom Schoonjans",
    author_email = "Tom.Schoonjans@gmail.com",
    description = "Utilities around the XRMC package",
    license = "GPLv3",
    url = "https://github.com/tschoonj/xrmc-utils/"

)
