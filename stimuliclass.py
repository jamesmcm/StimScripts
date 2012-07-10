from achrolab.printing import CalibDataFile
from achrolab.eyeone import EyeOne, EyeOneConstants
from ctypes import c_float
from contextlib import closing
from psychopy import visual
from psychopy import event
import eizoGS320
import math
import time
import mondrian
import Image
import numpy as np
from stimuli import *

class BaseMonitorTesting():
    """
    BaseMonitorTesting provides the basic methods for monitor testing - i.e. collecting data from the EyeOne, and presenting stimuli from images.
    """

    def __init__(self, usingeizo=False, measuring=False, calibrate=True, prefix="data", waittime=0.01):
        self.measuring=measuring
        self.usingeizo=usingeizo
        self.calibrate=calibrate
        self.prefix=prefix
        self.waittime=waittime

        if usingeizo==False:
            self.monitorsize=[1024,768]
            self.monitornum=0
            self.EyeOne = EyeOne.EyeOne(dummy=True) # EyeOne Object dummy

        else:
            self.monitorsize=[1024, 1536] #size of Eizo screen (half actualy monitor width)
            self.monitornum=1
            self.EyeOne = EyeOne.EyeOne(dummy=False) # Actual EyeOne Object


        if measuring==True:
            if(self.EyeOne.I1_SetOption(EyeOneConstants.I1_MEASUREMENT_MODE,
            EyeOneConstants.I1_SINGLE_EMISSION) == EyeOneConstants.eNoError):
                print("Measurement mode set to single emission.")
            else:
                print("Failed to set measurement mode.")
            if(self.EyeOne.I1_SetOption(EyeOneConstants.COLOR_SPACE_KEY,
                EyeOneConstants.COLOR_SPACE_CIExyY) == EyeOneConstants.eNoError):
                print("Color space set to CIExyY.")
            else:
                print("Failed to set color space.")

            # Initialization of spectrum and colorspace
            self.colorspace = (c_float * EyeOneConstants.TRISTIMULUS_SIZE)()
            self.spectrum = (c_float * EyeOneConstants.SPECTRUM_SIZE)()

            self.checkCalibrate()


    def checkCalibrate(self):
        if (self.calibrate or (self.EyeOne.I1_TriggerMeasurement() ==  EyeOneConstants.eDeviceNotCalibrated)):
        # Calibration of EyeOne
            print("\nPlease put EyeOne Pro on calibration plate and press \n key to start calibration.")
            while(self.EyeOne.I1_KeyPressed() != EyeOneConstants.eNoError):
                time.sleep(0.1)
            if (self.EyeOne.I1_Calibrate() == EyeOneConstants.eNoError):
                print("Calibration done.")
            else:
                print("Calibration failed.")

    def showStimuliFromPNG(self, inputfilename):
        self.window = visual.Window(self.monitorsize, monitor="mymon", color=eizoGS320.encode_color(0,0), screen=self.monitornum, colorSpace="rgb255", allowGUI=False, units="pix")
        self.imagestim=visual.SimpleImageStim(self.window, image=inputfilename, units='norm', pos=(0.0, 0.0), contrast=1.0, opacity=1.0, flipHoriz=False, flipVert=False, name='imagestim', autoLog=True)
        #Return function which handles drawing of stimuli, so we can write a general loop for all stimuli drawing/measurement
        #self.grayvals=None # specify in subclasses
        def drawFunction():
            self.imagestim.draw()
            self.window.flip()

        self.drawFunction=drawFunction

    def collectData(self, datafile):
        if(self.EyeOne.I1_TriggerMeasurement() != EyeOneConstants.eNoError):
            print("Measurement failed.")
            # retrieve Color Space
            if(self.EyeOne.I1_GetTriStimulus(self.colorspace, 0) != EyeOneConstants.eNoError):
                print("Failed to get color space.")
            else:
                print("Color Space " + str(self.colorspace[:]) + "\n")
                datafile.writeDataTXT(grayvals=self.grayvals, rgb=None, xyY=self.colorspace, voltage=None, spec_list=None, delimiter="\t")

    def runningLoop(self):
        #Abstract loop here
        running=True
        with closing(CalibDataFile(prefix=self.prefix)) as datafile:
            while running==True:
                keys=event.getKeys()
                for thiskey in keys:
                    if thiskey in ['q', 'escape']:
                        running=False
                        break

                self.drawFunction()
                if self.measuring==True:
                    self.collectData(datafile)
                time.sleep(self.waittime)


class CRTTest(BaseMonitorTesting):
    def __init__(self, usingeizo=False, measuring=False, calibrate=True,prefix="data", waittime=0.1, patchsize=0.5, centralstimgray=400, sinamplitude=1023, freq=0.01, sinoffset=0):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measuring=measuring, calibrate=calibrate, prefix=prefix, waittime=waittime)
        self.patchsize=patchsize
        self.centralstimgray=centralstimgray
        self.sinamplitude=sinamplitude
        self.freq=freq
        self.sinoffset=sinoffset
        self.graystim=0
        self.n=0

    def initdraw(self):
        self.window = visual.Window(self.monitorsize, monitor="mymon", color=eizoGS320.encode_color(0,0), winType="pygame", screen=self.monitornum, colorSpace="rgb255", allowGUI=False, units="pix")

        self.bgstim=visual.PatchStim(self.window, tex=None, units='norm', pos=(0, 0), size=2, colorSpace=self.window.colorSpace, color=eizoGS320.encode_color(0, 0))

        self.centralstim=visual.PatchStim(self.window, tex=None, units='norm', pos=(0, 0), size=self.patchsize, colorSpace=self.window.colorSpace, color=eizoGS320.encode_color(self.centralstimgray, self.centralstimgray))
        self.n=0
        self.grayvals=[self.graystim, self.centralstimgray]

    def drawFunction(self):
        #sinamplitude, freq, sinoffset
        self.graystim=(self.sinamplitude*abs(math.sin(2*math.pi*self.freq*self.n)))+self.sinoffset
        color=eizoGS320.encode_color(self.graystim, self.graystim)
        #color = [x/128.-1 for x in color]
        #mywin.setColor(color, 'rgb255')
        self.bgstim.setColor(color)
        self.n+=1
        self.n = self.n % (1./self.freq)
        self.bgstim.draw()
        self.centralstim.draw()
        self.window.flip()

    def run(self):
        self.initdraw()
        self.runningLoop()

class Mondrian(BaseMonitorTesting):
    ''' Produces Mondrian PNG if not provided, otherwise will display the Mondrian with run(). Still need to fix the unencoded version.'''

    def __init__(self, usingeizo=False, measuring=False, calibrate=True,prefix="data", waittime=0.1, highgray=1023, lowgray=0, step=1, meanlength=5, weights=None, accuracy=0.05, max_cycles=1000, write=False, pngfile=None, imagesize=None, encode=True):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measuring=measuring, calibrate=calibrate, prefix=prefix, waittime=waittime)
        if imagesize==None:
            mondriansize=self.monitorsize
        else:
            mondriansize=imagesize
        mondriansize.reverse()
        #Create mondrian if no PNG file provided
        if (pngfile==None) or (pngfile==""):
            colorlist=range(lowgray, highgray, step)
            nparray=mondrian.create_mondrian(mondriansize, meanlength, colorlist, weights, accuracy, max_cycles, write)
            if encode==True:
                nparray=eizoGS320.encode_np_array(nparray)
            else:
                #This is broken, must encode for now
                nparray=(1.0/4.0)*nparray
                nparray=nparray.view('uint8')[:,::4]
                #nparray.dtype = np.uint8
            pil_im = Image.fromarray(nparray)
            self.pngfile="mondrian"+time.strftime("%Y%m%d_%H%M")+".png"
            pil_im.save(self.pngfile)

        else:
            self.pngfile=pngfile

    def run(self):
        self.showStimuliFromPNG(self.pngfile)
        self.runningLoop()

class Cornsweet(BaseMonitorTesting):
    def __init__(self, usingeizo=False, measuring=False, calibrate=True,prefix="data", waittime=0.1, visualdegrees=None, ppd=128, contrast=1, ramp_width=3, exponent=2.75, mean_lum=511, pngfile=None, encode=True):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measuring=measuring, calibrate=calibrate, prefix=prefix, waittime=waittime)
        if pngfile==None:
            if visualdegrees==None:
                visualdegrees=[]
                visualdegrees.append(int(self.monitorsize[1]/ppd))
                visualdegrees.append(int(self.monitorsize[0]/ppd))
            nparray=cornsweet(visualdegrees, ppd, contrast, ramp_width, exponent, mean_lum)
            if encode==True:
                nparray=eizoGS320.encode_np_array(nparray)
            pil_im = Image.fromarray(nparray)
            self.pngfile="cornsweet"+time.strftime("%Y%m%d_%H%M")+".png"
            pil_im.save(self.pngfile)
        else:
            self.pngfile=pngfile

    def run(self):
        self.showStimuliFromPNG(self.pngfile)
        self.runningLoop()

class Todorovic(BaseMonitorTesting):
    def __init__(self, usingeizo=False, measuring=False, calibrate=True,prefix="data", waittime=0.1, visualdegrees=None, ppd=128, contrast=1, ramp_width=3, exponent=2.75, mean_lum=511, vert_rep=3, horz_rep=5, pngfile=None, encode=True):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measuring=measuring, calibrate=calibrate, prefix=prefix, waittime=waittime)
        if pngfile==None:
            if visualdegrees==None:
                visualdegrees=[]
                visualdegrees.append(int((self.monitorsize[1]/ppd)/vert_rep))
                visualdegrees.append(int((self.monitorsize[0]/ppd)/horz_rep))
            nparray=cornsweet(visualdegrees, ppd, contrast, ramp_width, exponent, mean_lum)
            nparray=todorovic(nparray, vert_rep, horz_rep)
            if encode==True:
                nparray=eizoGS320.encode_np_array(nparray)
            pil_im = Image.fromarray(nparray)
            self.pngfile="todorovic"+time.strftime("%Y%m%d_%H%M")+".png"
            pil_im.save(self.pngfile)
        else:
            self.pngfile=pngfile

    def run(self):
        self.showStimuliFromPNG(self.pngfile)
        self.runningLoop()

class WhiteIllusion(BaseMonitorTesting):
    def __init__(self, usingeizo=False, measuring=False, calibrate=True,prefix="data", waittime=0.1, kind="bmcc", visualdegrees=None, ppd=128, contrast=1, frequency=5, mean_lum=511, start='high', pngfile=None, encode=True):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measuring=measuring, calibrate=calibrate, prefix=prefix, waittime=waittime)
        if pngfile==None:
            if visualdegrees==None:
                visualdegrees=[]
                visualdegrees.append(int(self.monitorsize[1]/ppd))
                visualdegrees.append(int(self.monitorsize[0]/ppd))
            if kind=="bmcc":
                nparray=whites_illusion_bmcc(visualdegrees, ppd, contrast, frequency, mean_lum=mean_lum, start=start)
            if kind=="gil":
                nparray=whites_illusion_gil(visualdegrees, ppd, contrast, frequency, mean_lum=mean_lum, start=start)

            if encode==True:
                nparray=eizoGS320.encode_np_array(nparray)
            pil_im = Image.fromarray(nparray)
            self.pngfile="whiteillusion"+kind+time.strftime("%Y%m%d_%H%M")+".png"
            pil_im.save(self.pngfile)
        else:
            self.pngfile=pngfile
    def run(self):
        self.showStimuliFromPNG(self.pngfile)
        self.runningLoop()

class SquareWave(BaseMonitorTesting):
    def __init__(self, usingeizo=False, measuring=False, calibrate=True,prefix="data", waittime=0.1, visualdegrees=None, ppd=512, contrast=1, frequency=5, mean_lum=511, period='ignore', start='high', pngfile=None, encode=True):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measuring=measuring, calibrate=calibrate, prefix=prefix, waittime=waittime)
        if pngfile==None:
            if visualdegrees==None:
                visualdegrees=[]
                visualdegrees.append(int(self.monitorsize[1]/ppd))
                visualdegrees.append(int(self.monitorsize[0]/ppd))
            nparray=square_wave(visualdegrees, ppd, contrast, frequency, mean_lum, period=period, start=start)
            if encode==True:
                nparray=eizoGS320.encode_np_array(nparray)
            pil_im = Image.fromarray(nparray)
            self.pngfile="squarewave"+time.strftime("%Y%m%d_%H%M")+".png"
            pil_im.save(self.pngfile)
        else:
            self.pngfile=pngfile
    def run(self):
        self.showStimuliFromPNG(self.pngfile)
        self.runningLoop()

class Lines(BaseMonitorTesting):
    def __init__(self, usingeizo=False, measuring=False, calibrate=True,prefix="data", waittime=0.1, pngfiles=None, encode=True, monitorsize=None, lowgray=0, highgray=1023, linewidth=8):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measuring=measuring, calibrate=calibrate, prefix=prefix, waittime=waittime)
        self.linepngs=[]
        if pngfiles==None:
            if monitorsize==None:
                monitorsize=self.monitorsize
            monitorsize.reverse()
            nparrayx=np.ones(monitorsize, dtype=np.uint16)
            nparrayx*=512
            nparrayy=np.ones(monitorsize, dtype=np.uint16)
            nparrayy*=512
            i=0
            color=lowgray
            #x-loop
            while i<monitorsize[0]:
                if i%linewidth==0:
                    if color==lowgray:
                        color=highgray
                    else:
                        color=lowgray
                nparrayx[i, :]=color
                i+=1
            i=0
            #y-loop
            while i<monitorsize[1]:
                if i%linewidth==0:
                    if color==lowgray:
                        color=highgray
                    else:
                        color=lowgray
                nparrayy[:,i]=color
                i+=1
            if encode==True:
                nparrayx=eizoGS320.encode_np_array(nparrayx)
                nparrayy=eizoGS320.encode_np_array(nparrayy)

            pil_imx = Image.fromarray(nparrayx)
            pil_imy = Image.fromarray(nparrayy)
            timem=str(time.strftime("%Y%m%d_%H%M"))
            self.linepngs.append("linesx"+timem+".png")
            self.linepngs.append("linesy"+timem+".png")
            pil_imx.save(self.linepngs[0])
            pil_imy.save(self.linepngs[1])

        else:
            self.linepngs=pngfiles

    def drawFunction(self):
            if self.n%2 == 0:
                self.linesx.draw()
                print "Horizontal lines drawn"
            else:
                self.linesy.draw()
                print "Vertical lines drawn"
            self.n+=1
            self.n = self.n % 2
            self.window.flip()

    def run(self):
        self.window = visual.Window(self.monitorsize, monitor="mymon", color=eizoGS320.encode_color(0,0), screen=self.monitornum, colorSpace="rgb255", allowGUI=False, units="pix")
        self.linesx=visual.SimpleImageStim(self.window, image=self.linepngs[0], units='norm', pos=(0.0, 0.0), contrast=1.0, opacity=1.0, flipHoriz=False, flipVert=False, name='linesx', autoLog=True)
        self.linesy=visual.SimpleImageStim(self.window, image=self.linepngs[1], units='norm', pos=(0.0, 0.0), contrast=1.0, opacity=1.0, flipHoriz=False, flipVert=False, name='linesy', autoLog=True)
        self.n=0
        self.runningLoop()

class SinGrating(BaseMonitorTesting):
    '''
    Note this stimuli does not yet appear to work as intended.
     '''

    def __init__(self, usingeizo=False, measuring=False, calibrate=True,prefix="data", waittime=0.1, pngfiles=None, encode=True, monitorsize=None, gratingheight=20, sinamplitude=512, sinoffset=512):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measuring=measuring, calibrate=calibrate, prefix=prefix, waittime=waittime)

        self.sinpngs=[]
        if pngfiles==None:
            if monitorsize==None:
                monitorsize=self.monitorsize
            monitorsize.reverse()
            nparray0=np.ones(monitorsize, dtype=np.uint16)
            nparray0*=512
            nparray180=np.ones(monitorsize, dtype=np.uint16)
            nparray180*=512
            i=0
            #x-loop
            while i<monitorsize[1]:
                nparray0[int(monitorsize[0]/2)-gratingheight:int(monitorsize[0]/2)+gratingheight, i]=(sinamplitude*math.sin((((2.0*math.pi)/(monitorsize[1]))*i) +0.00001)) + sinoffset
                nparray180[int(monitorsize[0]/2)-gratingheight:int(monitorsize[0]/2)+gratingheight, i]=(sinamplitude*math.sin((((2.0*math.pi)/(monitorsize[1]))*i) +0.00001 + math.pi)) + sinoffset                
                i+=1

                
            if encode==True:
                nparray0=eizoGS320.encode_np_array(nparray0)
                nparray180=eizoGS320.encode_np_array(nparray180)

            pil_im0 = Image.fromarray(nparray0)
            pil_im180 = Image.fromarray(nparray180)
            timem=str(time.strftime("%Y%m%d_%H%M"))
            self.sinpngs.append("singrating0p"+timem+".png")
            self.sinpngs.append("singrating180p"+timem+".png")
            pil_im0.save(self.sinpngs[0])
            pil_im180.save(self.sinpngs[1])

        else:
            self.sinpngs=pngfiles

    def drawFunction(self):
        if self.n%2 == 0:
            self.sin0.draw()
            print "0 phase sin grating drawn"
        else:
            self.sin180.draw()
            print "180 phase sin grating drawn"
        self.n+=1
        self.n = self.n % 2
        self.window.flip()

    def run(self):
        self.window = visual.Window(self.monitorsize, monitor="mymon", color=eizoGS320.encode_color(0,0), screen=self.monitornum, colorSpace="rgb255", allowGUI=False, units="pix")
        self.sin0=visual.SimpleImageStim(self.window, image=self.sinpngs[0], units='norm', pos=(0.0, 0.0), contrast=1.0, opacity=1.0, flipHoriz=False, flipVert=False, name='phase0', autoLog=True)
        self.sin180=visual.SimpleImageStim(self.window, image=self.sinpngs[1], units='norm', pos=(0.0, 0.0), contrast=1.0, opacity=1.0, flipHoriz=False, flipVert=False, name='phase180', autoLog=True)
        self.n=0
        self.runningLoop()
