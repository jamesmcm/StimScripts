#Display instructions
#Load list of stimuli filenames
#display stimuli and cross
# get mouse event
#clear events
#save data
#Allow for blocks of data, resuming, etc



from achrolab.devtubes import DevTubes
from achrolab import printing
from contextlib import closing

from psychopy import core, visual, gui, misc, event
import time
import Image, ImageDraw, ImageFont
import eizoGS320



voltages = (1162, 1755, 1614)
bg = (155,155,17)       # 621


def trial(data, same, outputFile):
    # fixation cross
    cross = visual.SimpleImageStim(mywin, "cross.png", units="pix")

    cross.draw()
    #get filenames from data
    filename=data[0]

    stim= visual.SimpleImageStim(mywin, image=filename, units='norm', pos=(0.0, 0.0), contrast=1.0, opacity=1.0, flipHoriz=False, flipVert=False, name='stim', autoLog=True)


    stim.draw()
    mywin.flip()

    trialClock  = core.Clock() # to keep track of time during each trial
    exp_time = None
    exp_time = trialClock.getTime()

    # save keys
    thisResp = None
    while thisResp == None:
        for key in event.getKeys():
            if key in ['escape','q']:
                core.quit()
        mouse1, mouse2, mouse3 = mymouse.getPressed()

        if (same == 'left'):
            if (mouse1):
                thisResp = 's'
                rtTime = trialClock.getTime() - exp_time
                key = 'l'
            elif (mouse3):
                thisResp = 'd'
                rtTime = trialClock.getTime() - exp_time
                key = 'r'

        elif (same == 'right'):
            if (mouse1):
                thisResp = 'd'
                rtTime = trialClock.getTime() - exp_time
                key = 'l'
            elif (mouse3):
                thisResp = 's'
                rtTime = trialClock.getTime() - exp_time
                key = 'r'

        # time = trialClock.getTime()
        # if (time > 0.5):
        #     cross.draw()
        #     mywin.flip()
            # (nicht sehr effizient, da mywin kontinuierlich upgedatet wird
            # bis zur Reaktion -- bessere Loesung?)

        event.clearEvents() # must clear other events (like mouse movements)
        #    dataFile.write('%5.4s %5.4s %5.4s %5.4s %5.4s %5.4s %5.4s %7.4f %5.4s\n' %(config[0][0], config[0][1], config[0][2], config[1][0], config[1][1], config[1][2], thisResp, rtTime, key))
        outputFile.writeDataTXT(stimuliName=data[0], leftmean=data[1], leftvar=data[2], leftgrayplus=data[3], rightmean=data[5], rightvar=data[6], rightgrayplus=data[7], bg=bg, voltages=voltages, rtTime=rtTime, key=key, thisResp=thisResp, delimiter="\t")
    # show fixation cross the whole time
    cross.draw()
    mywin.flip()
    core.wait(2)    # ISI 2 sec in order to avoid influence of after image

def load_instructions(inputfile):
    im_draw = visual.SimpleImageStim(mywin, inputfile, units="pix")

    event.clearEvents()
    run = True
    while run:
        for key in event.getKeys():
            if key in ['escape','q']:
                core.quit()

        mouse1, mouse2, mouse3 = mymouse.getPressed()

        if (mouse1):
            run = False

        event.clearEvents()
            
        im_draw.draw()
        mywin.flip()
        
    mywin.flip()
    core.wait(0.5)

def new_block(input):
    im = Image.new("RGB", (2048, 500), bg)
    
    font = ImageFont.truetype("arial.ttf", 50)
    draw = ImageDraw.Draw(im)
    draw.text((580, 100), input, fill=(0,0,0), font=font)
    # Attention: input can only be one line!
    draw.text((580, 200), 'Weiter mit linker Maustaste.', fill=(0,0,0), font=font)
    im.save("instructions/new_block.png")

    eizoGS320.convert_to_eizo_picture("instructions/new_block.png", "instructions/block_eizo.png")
    
    im_draw = visual.SimpleImageStim(mywin, "instructions/block_eizo.png", units="pix")

    event.clearEvents()
    run = True
    while run:
        for key in event.getKeys():
            if key in ['escape','q']:
                core.quit()

        mouse1, mouse2, mouse3 = mymouse.getPressed()

        if (mouse1):
            run = False

        event.clearEvents()
            
        im_draw.draw()
        mywin.flip()
        
    mywin.flip()
    core.wait(0.5)



# try to load last expInfos
try:
    expInfo = misc.fromFile('last_expInfo.pickle')
except:
    expInfo = {'Versuchsleiter':'noum', 'Versuchsperson':'vp01', 'Session':'ses01', 'Sessionfile':'session/vp01ses01.txt'}

expInfo['Datum'] = time.strftime("%Y%m%d_%H%M", time.localtime())

# present a dialogue to change infos
dlg = gui.DlgFromDict(expInfo, title='same/different Exp', fixed=['Datum'])
if dlg.OK:
    misc.toFile('last_expInfo.pickle', expInfo)
    # save params to file for next time
else:
    core.quit()
    # the user hit cancel so exit

# create window, mouse and clock

mywin = visual.Window([1024,1536], monitor='mymon', color=bg,
        allowGUI=False, screen=1, colorSpace='rgb255')
mymouse = event.Mouse(win=mywin)

# set tubes
tub = DevTubes()
tub.setVoltages(voltages)

# make a text file to save data
with closing(printing.ExperimentDataFile(expInfo)) as outputFile:
    #Do experiment stuff
    execfile(expInfo['Sessionfile']) #maybe change this

# quit program
mywin.close()
core.quit()

