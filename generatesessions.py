#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import random

#random.seed(1)
currentsession=1
headerstr="#!/usr/bin/env python\n# -*- encoding: utf-8 -*-\n"
stimulilistncfilename="stimulilistac20120801_1211.txt"
stimulilistacfilename=stimulilistncfilename.replace("nc","ac")
#stimulilistacfilename="stimulilistac20120725_1421.txt"
#3920
nviewsperstimuli=80
nsubjects=2
nblocks=56 #per session
nviewsperblock=10
nsessions=7
direction="left" #automatically alternated
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
if (nviewsperstimuli*nstimac)!=(nblocks*nviewsperblock*nsessions):
    raise ValueError("Number of stimuli multiplied by views per stimuli did not equal the number of blocks multiplied by the number of views in a block multiplied by the number of sessions.")

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

while n<=nsubjects:
    #Sample without replacement all stimuli
    samplelistac=random.sample(stimulilistac, nviewsperblock*nblocks*nsessions)
    samplelistnc=random.sample(stimulilistnc, nviewsperblock*nblocks*nsessions)
    totalsum=0

    if n%2==1: #alternate left/right with changing subjects
        direction="left"
    else:
        direction="right"
    print n
    while currentsession<=nsessions:
        sessionac=open("sessions/sessionac_"+str(currentsession)+"_"+stimulilistacfilename[13:-4]+"subject"+str(n)+".txt", "w")
        sessionnc=open("sessions/sessionnc_"+str(currentsession)+"_"+stimulilistncfilename[13:-4]+"subject"+str(n)+".txt", "w")

        #Training blocks
        sessionac.write(headerstr)
        sessionnc.write(headerstr)
        sessionac.write("load_instructions('instructions/instructions1.png')\nload_instructions('instructions/instructions2_"+str(direction)+".png')\nload_instructions('instructions/instructions3.png')\n")
        sessionnc.write("load_instructions('instructions/instructions1.png')\nload_instructions('instructions/instructions2_"+str(direction)+".png')\nload_instructions('instructions/instructions3.png')\n") #alternate left and right

        trainsamplelistac=random.sample(stimulilistac, nviewsperblock*2)
        trainsamplelistnc=random.sample(stimulilistnc, nviewsperblock*2)
        for z in range(nviewsperblock):
            sampleacstr=str(trainsamplelistac[z])
            samplencstr=str(trainsamplelistnc[z])
            if direction=="right":
                sampleacstr=sampleacstr.replace("left","right")
                samplencstr=samplencstr.replace("left","right")
            sessionac.write(sampleacstr+"\n")
            sessionnc.write(samplencstr+"\n")
        sessionac.write("new_block(u'Pause.')\n")
        sessionnc.write("new_block(u'Pause.')\n")
        #second training block
        for z in range(nviewsperblock):
            sampleacstr=str(trainsamplelistac[z+nviewsperblock])
            samplencstr=str(trainsamplelistnc[z+nviewsperblock])
            if direction=="right":
                sampleacstr=sampleacstr.replace("left","right")
                samplencstr=samplencstr.replace("left","right")
            sessionac.write(sampleacstr+"\n")
            sessionnc.write(samplencstr+"\n")
        sessionac.write("load_instructions('instructions/ende_training_"+str(direction)+".png')\n")
        sessionnc.write("new_block(u'Pause.')\n")

        for k in range(nblocks):
            #take first nviewsperblock of samplelist and then print pause - also write code for practice tests, and with progress indicator etc. from Noras sessions
            for l in range(nviewsperblock):
                sampleacstr=str(samplelistac[totalsum])
                samplencstr=str(samplelistnc[totalsum])
                totalsum+=1
                if direction=="right":
                    sampleacstr=sampleacstr.replace("left","right")
                    samplencstr=samplencstr.replace("left","right")
                sessionac.write(sampleacstr+"\n")
                sessionnc.write(samplencstr+"\n")
            sessionac.write("new_block(u'Pause. Block " +str(k+1)+ " von "+str(nblocks)+ " Blöcken geschafft!')\n")
            sessionnc.write("new_block(u'Pause. Block " +str(k+1)+ " von "+str(nblocks)+ " Blöcken geschafft!')\n")

        sessionac.write("load_instructions('instructions/ende.png')")
        sessionnc.write("load_instructions('instructions/ende.png')")
        sessionnc.close()
        sessionac.close()
        currentsession+=1
    n+=1
    currentsession=1
