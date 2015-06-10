## Installation instruction

Install the XRMC python reader with:

````
python setup.py install
````

This will also download and install the `numpy` and `matplotlib` dependencies, if necessary.
We recommend using python 3.x for this, although python 2.7 should work too.

##Usage

````
xrmc-plot [-h] [--ScatOrderNum SCATORDERNUM] xrmc-output-file
````

with `SCATORDERNUM` set to the required interaction order. If no value is provided, then the sum will be plotted over all interactions.
Ensure that the `detector.dat` file used in the simulation had `HeaderFlag` set to 1!!!

## Uninstall

Use `pip` (the one that corresponds to the python version you used for the installation) for this purpose:

````
pip uninstall xrmc
````


