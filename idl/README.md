To use `xrmc_read_output.pro` from IDL:

  1. Copy this file somewhere it will be get picked up by IDL, which means a location that is covered by the `IDL_PATH` environment variable, or the current working directory
  2. Launch IDL
  3. Assuming your file is called `output.dat`, call the `XRMC_READ_OUTPUT` function:
     * If the detector file contained `HeaderFlag 1`: `var = XRMC_READ_OUTPUT('output.dat')`
     * If the detector file contained `HeaderFlag 0` (or if the HeaderFlag keyword is left out): `var = XRMC_READ_OUTPUT('output.dat', ModeNum, NX, NY, NBins)`, with ModeNum equal to the `ScattOrderNum` parameter in the sample file increased by 1, NX and NY the number of pixels on the detector in both orientations and NBins equal to the number of channels defined by `NBins` in the detector file.
