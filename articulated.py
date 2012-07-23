from stimuliclass import Mondrian
import numpy as np
import Image
import time
import eizoGS320

k=0
timeset=time.strftime("%Y%m%d_%H%M", time.localtime())
fileout=open("sessionfile"+str(timeset)+".txt", "w")
while k<5:
    monitorsize=[2048, 1536]
    mondheight=monitorsize[1]/2.0
    mondwidth=monitorsize[0]/4.0
    bggray=621

    leftweightsvar=256.0
    leftweightsmean=512+k

    rightweightsvar=256.0
    rightweightsmean=512+k

    leftgrayminus=400
    rightgrayminus=400

    seedleft=1
    seedright=1

    leftweights=[]
    for i in range(1023):
        leftweights.append(((1.0/(leftweightsvar * np.sqrt(2*np.pi))) * np.exp(-0.5*(((i-leftweightsmean)/leftweightsvar)**2))))

    rightweights=[]
    for i in range(1023):
        rightweights.append(((1.0/(rightweightsvar * np.sqrt(2*np.pi))) * np.exp(-0.5*(((i-rightweightsmean)/rightweightsvar)**2))))


    rightweights=rightweights/sum(rightweights)
    leftweights=leftweights/sum(leftweights)

    bigarray=np.ones((monitorsize[1], monitorsize[0]))
    bigarray=bggray*bigarray

    #Draw Mondrian surrounds
    mymondleft=Mondrian(usingeizo=False, imagesize=[mondwidth, mondheight], encode=False, weights=leftweights, saveimage=False, seed=seedleft)

    bigarray[(monitorsize[1]/2.0)-mondheight/2.0:(monitorsize[1]/2.0)+mondheight/2.0,(monitorsize[0]/4.0)-mondwidth/2.0:(monitorsize[0]/4.0)+mondwidth/2.0] = mymondleft.mondrianarray

    mymondright=Mondrian(usingeizo=False, imagesize=[mondwidth, mondheight], encode=False, weights=rightweights, saveimage=False, seed=seedright)

    bigarray[(monitorsize[1]/2.0)-mondheight/2.0:(monitorsize[1]/2.0)+mondheight/2.0,(3*monitorsize[0]/4.0)-mondwidth/2.0:(3*monitorsize[0]/4.0)+mondwidth/2.0] = mymondright.mondrianarray

    #Overlay transparent insets
    bigarray[(monitorsize[1]/2.0)-(mondheight/4.0):(monitorsize[1]/2.0)+(mondheight/4.0),(3*monitorsize[0]/4.0)-(mondwidth/4.0):(3*monitorsize[0]/4.0)+(mondwidth/4.0)] -= rightgrayminus
    bigarray[(monitorsize[1]/2.0)-(mondheight/4.0):(monitorsize[1]/2.0)+(mondheight/4.0),(monitorsize[0]/4.0)-(mondwidth/4.0):(monitorsize[0]/4.0)+(mondwidth/4.0)] -= leftgrayminus


    bigarray[bigarray>1023]=1023
    bigarray[bigarray<0]=0

    # (N, M) = np.shape(bigarray)
    # newarray = np.zeros((N, M, 3), dtype=np.uint8)
    # newarray[:,:,0]=np.uint8(bigarray[:,:]/4)
    # newarray[:,:,1]=np.uint8(bigarray[:,:]/4)
    # newarray[:,:,2]=np.uint8(bigarray[:,:]/4)
    newarray=eizoGS320.encode_np_array(bigarray)
    pil_im = Image.fromarray(newarray)
    pngfile=str(leftweightsmean)+"_"+str(leftweightsvar)+"_"+str(rightweightsmean)+"_"+str(rightweightsvar)+"_"+str(bggray)+".png"

    fileout.write("trial(['"+str(leftweightsmean)+"_"+str(leftweightsvar)+"_"+str(rightweightsmean)+"_"+str(rightweightsvar)+"_"+str(bggray)+".png', "+str(leftweightsmean)+","+str(leftweightsvar)+","+str(leftgrayminus)+","+str(rightweightsmean)+","+str(rightweightsvar)+","+str(rightgrayminus)+","+str(bggray)+"])\n")
    pil_im.save(pngfile)
    k+=1

fileout.close()
