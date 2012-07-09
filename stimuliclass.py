from achrolab.printing import CalibDataFile
from achrolab.eyeone import EyeOne, EyeOneConstants
from ctypes import c_float
from contextlib import closing
from psychopy import visual
from psychopy import event
import eizoGS320
import math
import time
import eizoGS320

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


        if measurement==True:
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
            while running:
                keys=event.getKeys()
                for thiskey in keys:
                    if thiskey in ['q', 'escape']:
                        running=False
                        break

                self.drawFunction(self.drawarguments)
                if self.measuring==True:
                    self.collectData(datafile)
                time.sleep(self.waittime)




class CRTTest(BaseMonitorTesting):
    def __init__(self, usingeizo=False, measurement=False, calibrate=True,prefix="data", waittime=0.1, patchsize=0.5, centralstimgray=400):
        BaseMonitorTesting.__init__(self, usingeizo=usingeizo, measurement=measurement, calibrate=calibrate, prefix=prefix, waittime=waittime)
        self.patchsize=patchsize
        self.centralstimgray=centralstimgray

    def initdraw(self):
        self.window = visual.Window(self.monitorsize, monitor="mymon", color=eizoGS320.encode_color(0,0), winType="pygame", screen=self.monitornum, colorSpace="rgb255", allowGUI=False, units="pix")

        self.bgstim=visual.PatchStim(self.window, tex=None, units='norm', pos=(0, 0), size=2, colorSpace=self.window.colorSpace, color=eizoGS320.encode_color(0, 0))

        self.centralstim=visual.PatchStim(self.window, tex=None, units='norm', pos=(0, 0), size=self.patchsize, colorSpace=self.window.colorSpace, color=eizoGS320.encode_color(self.centralstimgray, self.centralstimgray))

        



