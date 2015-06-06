import numpy as np
import struct
import matplotlib.pyplot as plt

class Output:
    """ A class whose instances will represent XRMC output files"""
    def __init__(self, filename, ModeNum=None, NX=None, NY=None, NBins=None):
        """Initialization function"""
        self.filename = filename
        with open(filename, 'rb') as f:
            if (ModeNum != None and NX != None and NY != None and NBins != None):
                self.ModeNum = ModeNum
                self.NX = NX
                self.NY = NY
                self.NBins = NBins
            else:
                raw = f.read(20+40)
                toupee = struct.unpack('=iiidddiidd', raw)
                self.ModeNum = toupee[0]
                self.NX = toupee[1]
                self.NY = toupee[2]
                self.PixelSizeX = toupee[3]
                self.PixelSizeY = toupee[4]
                self.ExpTime = toupee[5]
                self.PixelType = toupee[6]
                self.NBins= toupee[7]
                self.Emin= toupee[8]
                self.Emax= toupee[9]
            # now the numpy part
            data = np.fromfile(f, dtype=np.double)
            if (len(data) != self.ModeNum * self.NX * self.NY * self.NBins):
                raise OSError('number of read bytes not matching expected value')
        data = data.reshape(self.ModeNum, self.NBins, self.NY, self.NX)
        self.data = data

    def plot(self, ScatOrderNum = None):
        if (ScatOrderNum != None and (ScatOrderNum > self.ModeNum -1 or ScatOrderNum < 0)):
            raise IndexError('ScatOrderNum out of range. Must be smaller than '+self.ModeNum)
        my_shape = self.data.shape
        if (my_shape[2] == 1 and my_shape[3] == 1):
            # Case 1: spectrum plot
            if (ScatOrderNum == None):
                # integrate
                data = self.data[:,:,0,0].sum(0)
            else:
                data = self.data[ScatOrderNum,:,0,0]
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
                data = self.data.sum(0).sum(0)
            else:
                data = self.data[ScatOrderNum,:,:,:].sum(1)
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


        
