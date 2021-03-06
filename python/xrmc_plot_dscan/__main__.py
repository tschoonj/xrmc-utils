#!/usr/bin/env python3

import argparse
import xrmc
import sys
import numpy
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='Plots XRMC dscan results')
    parser.add_argument('--ScatOrderNum', type=int, help='Plot only contribution for N interactions. Default is to sum over all contributions.', metavar='N')
    parser.add_argument('--XRFline', type=str, help='Plot only contribution for a given fluorescence line. Example: Fe-Ka or Pb-L3M5')
    parser.add_argument('--prefix', type=str, help='File prefix (may include path) PREFIX', default='output_convolutedimage_', metavar='PREFIX')
    parser.add_argument('--write-to-csv', type=str, help='Write plot to CSV file FILENAME', metavar='FILENAME')
    parser.add_argument('axis', type=str, help='The name of the motoraxis used in the dscan', choices=['x', 'y', 'z'])
    parser.add_argument('start_value', type=float, help='The starting value of the dscan')
    parser.add_argument('end_value', type=float, help='The ending value of the dscan')
    parser.add_argument('n_steps', type=int, help='The number of steps it takes the dscan to get from start_value to end_value')
    args = parser.parse_args()

    if (vars(args)['ScatOrderNum'] != None and vars(args)['ScatOrderNum'] < 0):
        print('ScatOrderNum must be greater than or equal to zero')
        sys.exit(1)

    if (vars(args)['start_value'] >= vars(args)['end_value']):
        print('start_value must be less than end_value!')
        sys.exit(1)

    if (vars(args)['n_steps'] < 1):
        print('n_steps must be greater than zero!')
        sys.exit(1)

    #print(vars(args))

    try:
        x_vals = numpy.arange(vars(args)['n_steps'] + 1, dtype=numpy.double) * (vars(args)['end_value'] - vars(args)['start_value']) / vars(args)['n_steps'] + vars(args)['start_value']
        #print(x_vals)
        y_vals = numpy.empty(vars(args)['n_steps'] + 1, dtype=numpy.double) 
        for i in range(0,vars(args)['n_steps'] + 1):
            filename = vars(args)['prefix']+str(i)+'.dat'
            #print(filename)
            obj = xrmc.Output(filename)
            #if obj.NX != obj.NY != 1:
            #    raise ValueError(filename + ': detector pixels should be equal to 1 in both directions')
            bin_scope = None

            if (vars(args)['XRFline'] != None):
                bin_scope = obj.get_roi_from_XRF_line(vars(args)['XRFline'])
            else:
                bin_scope = slice(0, obj.NBins-1)

            if (vars(args)['ScatOrderNum'] != None):
                if (vars(args)['ScatOrderNum'] > obj.NodeNum -1):
                    raise IndexError('ScatOrderNum out of range. Must be smaller than '+str(obj.ModeNum))
                y_vals[i] = obj[vars(args)['ScatOrderNum'],bin_scope,:,:].sum()
            else:
                y_vals[i] = obj[:,bin_scope,:,:].sum()
        #print(y_vals)
        if vars(args)['write_to_csv'] is not None:
            numpy.savetxt(vars(args)['write_to_csv'], numpy.c_[x_vals, y_vals], delimiter=',')

        plt.plot(x_vals, y_vals, color='blue', lw=2)
        plt.xlabel('Motor-axis '+vars(args)['axis']+' position')
        plt.ylabel('Counts')
        plt.title('xrmc-dscan')
        plt.show()


    except Exception as e:
        print('Exception caught: ' + str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
