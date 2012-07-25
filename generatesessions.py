import random

#random.seed(1)

stimulilistncfilename="stimulilistnc20120725_1421.txt"
stimulilistacfilename="stimulilistac20120725_1421.txt"
nviewsperstimuli=2
nsubjects=2
nblocks=3
nviewsperblock=6

#####################

fnc=open(stimulilistncfilename, "r")
fac=open(stimulilistacfilename, "r")

stimulilistnc=fnc.readlines()
stimulilistac=fac.readlines()

nstimnc=len(stimulilistnc)#9
nstimac=len(stimulilistac) #Should equal eachother
print nstimac
if (nstimnc != nstimac):
    raise ValueError("Number of stimuli did not match")



#nviews*stimuli = nblocks*nviewsperblock
if (nviewsperstimuli*nstimac)!=(nblocks*nviewsperblock):
    raise ValueError("Number of stimuli multiplied by views per stimuli did not equal the number of blocks multiplied by the number of views in a block.")

#multiply up original list
i=0
j=0
while i<nstimac:
    while j<nviewsperstimuli-1:
        stimulilistac.append(stimulilistac[i])
        j+=1
    i+=1
    j=0

i=0
j=0
while i<nstimnc:
    while j<nviewsperstimuli-1:
        stimulilistnc.append(stimulilistnc[i])
        j+=1
    i+=1
    j=0
n=1

while n<nsubjects:
    sessionac=open("sessionac"+stimulilistacfilename[13:]+"subject"+str(n), "w")

    sessionac.write("load_instructions('instructions/instructions1.png')\nload_instructions('instructions/instructions2_left.png')\nload_instructions('instructions/instructions3.png')\n")
    samplelist=random.sample(stimulilistac, nviewsperblock*nblocks)

    #Sample without replacement
    for k in range(nblocks):
        #take first nviewsperblock of samplelist and then print pause - also write code for practice tests, and with progress indicator etc. from Noras sessions
        pass

    n+=1
