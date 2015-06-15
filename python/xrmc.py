import numpy as np
import struct
import matplotlib.pyplot as plt
import xraylib


class Output(np.ndarray):
    """ A class whose instances will represent XRMC output files as numpy arrays.
        Users are strongly encouraged to exploit the numpy API as much as possible"""
    def __new__(cls, filename, ModeNum=None, NX=None, NY=None, NBins=None):
        """Initialization function"""
        obj = None
        PixelSizeX = None
        PixelSizeY = None
        ExpTime = None
        PixelType = None
        Emin = None
        Emax = None
        with open(filename, 'rb') as f:
            if (ModeNum == None and NX == None and NY == None and NBins == None):
                raw = f.read(20+40)
                toupee = struct.unpack('=iiidddiidd', raw)
                ModeNum = toupee[0]
                NX = toupee[1]
                NY = toupee[2]
                PixelSizeX = toupee[3]
                PixelSizeY = toupee[4]
                ExpTime = toupee[5]
                PixelType = toupee[6]
                NBins= toupee[7]
                Emin= toupee[8]
                Emax= toupee[9]
            # now the numpy part
            obj = np.fromfile(f, dtype=np.double)
        if (len(obj) != ModeNum * NX * NY * NBins):
            raise OSError('number of read bytes not matching expected value')
        obj = obj.reshape(ModeNum, NBins, NY, NX).view(cls)
        obj.filename = filename
        obj.ModeNum = ModeNum
        obj.NX = NX
        obj.NY = NY
        obj.NBins = NBins
        if PixelSizeX is not None:
            obj.PixelSizeX = PixelSizeX 
        if PixelSizeY is not None:
            obj.PixelSizeY = PixelSizeY
        if ExpTime is not None:
            obj.ExpTime = ExpTime
        if PixelType is not None:
            obj.PixelType = PixelType
        if Emin is not None:
            obj.Emin = Emin 
        if Emax is not None:
            obj.Emax = Emax
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        if hasattr(obj, 'PixelSizeX'):
            self.PixelSizeX = getattr(obj, PixelSizeX)
        if hasattr(obj, 'PixelSizeY'):
            self.PixelSizeY = getattr(obj, PixelSizeY)
        if hasattr(obj, 'ExpTime'):
            self.ExpTime = getattr(obj, ExpTime)
        if hasattr(obj, 'PixelType'):
            self.PixelType= getattr(obj, PixelType)
        if hasattr(obj, 'Emin'):
            self.Emin = getattr(obj, Emin)
        if hasattr(obj, 'Emax'):
            self.Emax = getattr(obj, Emax)
        if hasattr(obj, 'filename'):
            self.filename = getattr(obj, filename)

    def write_to_csv(self, filename, ScatOrderNum = None):
        """Write the object contents to a CSV file,
           following the same conventions as plot"""
        #print("Entering write_to_csv")
        if (ScatOrderNum != None and (ScatOrderNum > self.ModeNum -1 or ScatOrderNum < 0)):
            raise IndexError('ScatOrderNum out of range. Must be smaller than '+str(self.ModeNum))

        my_shape = self.shape
        
        if (my_shape[2] == 1 and my_shape[3] == 1):
            # Case 1: spectrum plot
            if (ScatOrderNum == None):
                # integrate
                data = self[:,:,0,0].sum(0)
            else:
                data = self[ScatOrderNum,:,0,0]
        else:
            # Case 2: image
            if (ScatOrderNum == None):
                # integrate
                data = self.sum(0).sum(0)
            else:
                data = self[ScatOrderNum,:,:,:].sum(0)
        np.savetxt(filename, data, delimiter=',')
        

    def plot(self, ScatOrderNum = None):
        """Plot the object using Matplotlib. Use ScatOrderNum to select a particular
           interaction order. The default behaviour is to sum over all interactions"""
        if (ScatOrderNum != None and (ScatOrderNum > self.ModeNum -1 or ScatOrderNum < 0)):
            raise IndexError('ScatOrderNum out of range. Must be smaller than '+str(self.ModeNum))
        my_shape = self.shape
        if (my_shape[2] == 1 and my_shape[3] == 1):
            # Case 1: spectrum plot
            if (ScatOrderNum == None):
                # integrate
                data = self[:,:,0,0].sum(0)
            else:
                data = self[ScatOrderNum,:,0,0]
            data[data < 0.1] = 0.1
            if (hasattr(self, 'Emax')):
                energies = np.arange(self.NBins)*(self.Emax-self.Emin)/self.NBins + self.Emin
                xlabel = 'Energy (keV)'
            else:
                energies = np.arange(self.NBins)
                xlabel = 'Channel number'
            #plt.subplot(2,1,1)
            plt.plot(energies, data, color='blue', lw=2)
            plt.yscale('log')
            plt.xlabel('Energy (keV)')
            plt.ylabel('Counts')
            plt.title(self.filename)
            plt.show()
        else:
            # Case 2: image
            if (ScatOrderNum == None):
                # integrate
                data = self.sum(0).sum(0)
            else:
                data = self[ScatOrderNum,:,:,:].sum(0)
            fig = plt.figure(figsize=(6, 3.2))
            ax = fig.add_subplot(111)
            ax.set_title(self.filename)
            plt.imshow(data)
            ax.set_aspect('equal')
            cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
            cax.get_xaxis().set_visible(False)
            cax.get_yaxis().set_visible(False)
            cax.patch.set_alpha(0)
            cax.set_frame_on(False)
            plt.colorbar(orientation='vertical')
            plt.show()

    def get_roi_from_XRF_line(self,XRFline):
        """This function determines the region of interest that
        should be used to represent an XRF line"""

        # first thing to do is determine which element and line we are dealing with
        # split the string along the dash
        try:
            (element, line) = XRFline.split('-')
            #print('element: ' + element)
            #print('line: ' + line)

            atomic_number = xraylib.SymbolToAtomicNumber(element)
            if (atomic_number == 0):
                raise ValueError(element + ' could not be parsed by xraylib.SymbolToAtomicNumber')
            #print('atomic_number:' + str(atomic_number))

            # I can probably also get the same result with 'vars'
            line_macro = xraylib.__dict__[line.upper() + '_LINE']
            #print('line_macro:' + str(line_macro))

            line_energy = xraylib.LineEnergy(atomic_number, line_macro)
            #print('line_energy: ' + str(line_energy))
            if (line_energy == 0.0):
                raise ValueError('XRF line '+XRFline+' does not exist in the xraylib database')

            if (self.PixelType != 2):
                raise ValueError('get_roi_from_XRF_line requires that the object has PixelType 2')

            channel = int(self.NBins * (line_energy - self.Emin)/(self.Emax - self.Emin))
            #print('channel:' + str(channel))
            if (channel < 0 or channel >= self.NBins):
                raise ValueError('requested XRF line not covered by spectrum')

            return slice(max(0, channel - 10), min(self.NBins-1, channel + 10))

        except Exception as e:
            raise Exception(str(e))

        
