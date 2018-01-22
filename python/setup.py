from setuptools import setup, find_packages
import sys

#a crude test that ensures xraylib is installed...
try:
    import xraylib
except ImportError:
    print("Could not detect xraylib-python bindings. Ensure these are installed before continuing")
    sys.exit(1)

setup(
    name = "xrmc",
    version = "6.6.0",
    py_modules = ['xrmc', 'xrmc_plot.__main__', 'xrmc_plot_dmesh.__main__', 'xrmc_plot_dscan.__main__'],
    entry_points = {
        "console_scripts": [
            "xrmc-plot = xrmc_plot.__main__:main",
            "xrmc-plot-dmesh = xrmc_plot_dmesh.__main__:main",
            "xrmc-plot-dscan = xrmc_plot_dscan.__main__:main",
        ]
    },
    requires = ['numpy', 'matplotlib'],
    install_requires = ['numpy', 'matplotlib'],

    author = "Tom Schoonjans",
    author_email = "Tom.Schoonjans@gmail.com",
    description = "Utilities around the XRMC package",
    license = "GPLv3",
    url = "https://github.com/tschoonj/xrmc-utils/"

)
