#!/usr/bin/env python3

import argparse
import xrmc
import sys
import numpy
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='Plots XRMC dmesh results')
    parser.add_argument('--ScatOrderNum', type=int, help='Plot only contribution for N interactions. Default is to sum over all contributions.', metavar='N')
    parser.add_argument('--XRFline', type=str, help='Plot only contribution for a given fluorescence line. Example: Fe-Ka or Pb-L3M5')
    parser.add_argument('--transpose', action='store_true', default=False)
    parser.add_argument('--prefix', type=str, help='File prefix (may include path) PREFIX', default='output_convolutedimage_', metavar='PREFIX')
    parser.add_argument('--write-to-csv', type=str, help='Write plot to CSV file FILENAME', metavar='FILENAME')
    parser.add_argument('axis1', type=str, help='The name of the first motoraxis used in the dmesh', choices=['x', 'y', 'z'])
    parser.add_argument('start_value1', type=float, help='The starting value of the first motoraxis')
    parser.add_argument('end_value1', type=float, help='The ending value of the first motoraxis')
    parser.add_argument('n_steps1', type=int, help='The number of steps it takes for the first motor to get from start_value1 to end_value1')
    parser.add_argument('axis2', type=str, help='The name of the second motoraxis used in the dmesh', choices=['x', 'y', 'z'])
    parser.add_argument('start_value2', type=float, help='The starting value of the second motoraxis')
    parser.add_argument('end_value2', type=float, help='The ending value of the second motoraxis')
    parser.add_argument('n_steps2', type=int, help='The number of steps it takes for the second motor to get from start_value2 to end_value2')
    args = parser.parse_args()

    if (vars(args)['ScatOrderNum'] != None and vars(args)['ScatOrderNum'] < 0):
        print('ScatOrderNum must be greater than or equal to zero')
        sys.exit(1)

    if (vars(args)['axis1'] == vars(args)['axis2']):
        print('axis1 and axis2 have to be different!')
        sys.exit(1)

    if (vars(args)['start_value1'] >= vars(args)['end_value1']):
        print('start_value1 must be less than end_value1!')
        sys.exit(1)

    if (vars(args)['n_steps1'] < 1):
        print('n_steps1 must be greater than zero!')
        sys.exit(1)

    if (vars(args)['start_value2'] >= vars(args)['end_value2']):
        print('start_value2 must be less than end_value2!')
        sys.exit(1)

    if (vars(args)['n_steps2'] < 1):
        print('n_steps2 must be greater than zero!')
        sys.exit(1)


    #print(vars(args))

    try:
        x_vals1 = numpy.arange(vars(args)['n_steps1'] + 1, dtype=numpy.double) * (vars(args)['end_value1'] - vars(args)['start_value1']) / vars(args)['n_steps1'] + vars(args)['start_value1']
        x_vals2 = numpy.arange(vars(args)['n_steps2'] + 1, dtype=numpy.double) * (vars(args)['end_value2'] - vars(args)['start_value2']) / vars(args)['n_steps2'] + vars(args)['start_value2']
        #print(x_vals)
        y_vals = numpy.empty([vars(args)['n_steps1'] + 1, vars(args)['n_steps2'] + 1], dtype=numpy.double) 

        for i in range(0,vars(args)['n_steps1'] + 1):
            for j in range(0,vars(args)['n_steps2'] + 1):
                filename = vars(args)['prefix'] + str(i)+'_' + str(j)+'.dat'
                #print(filename)
                obj = xrmc.Output(filename)
                #if obj.NX != obj.NY != 1:
                #    raise ValueError(filename + ': detector pixels should be equal to 1 in both directions')
                bin_scope = None

                if (vars(args)['XRFline'] is not None):
                    bin_scope = obj.get_roi_from_XRF_line(vars(args)['XRFline'])
                else:
                    bin_scope = slice(0, obj.NBins-1)

                if (vars(args)['ScatOrderNum'] != None):
                    if (vars(args)['ScatOrderNum'] > obj.NodeNum -1):
                        raise IndexError('ScatOrderNum out of range. Must be smaller than '+str(obj.ModeNum))
                    y_vals[i,j] = obj[vars(args)['ScatOrderNum'],bin_scope,:,:].sum()
                else:
                    y_vals[i,j] = obj[:,bin_scope,:,:].sum()


        extent = None
        if vars(args)['transpose'] == True:
            y_vals = y_vals.transpose()
            extent = [vars(args)['start_value1'], vars(args)['end_value1'], vars(args)['start_value2'], vars(args)['end_value2']]
        else:
            extent = [vars(args)['start_value2'], vars(args)['end_value2'], vars(args)['start_value1'], vars(args)['end_value1']]

        if vars(args)['write_to_csv'] is not None:
            numpy.savetxt(vars(args)['write_to_csv'], y_vals, delimiter=',')

        fig = plt.figure(figsize=(6, 3.2))
        ax = fig.add_subplot(111)
        ax.set_title('xrmc-dmesh')
        plt.imshow(y_vals, origin='lower', extent=extent)
        ax.set_aspect('equal')
        cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical')
        plt.xlabel('motor axis '+ vars(args)['axis2'])
        plt.ylabel('motor axis '+ vars(args)['axis1'])
        plt.show()

    except Exception as e:
        print('Exception caught: ' + str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
