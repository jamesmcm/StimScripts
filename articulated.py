from stimuliclass import Mondrian
import numpy as np
import Image
import time

monitorsize=[2048, 1536]
mondheight=monitorsize[1]/2.0
mondwidth=monitorsize[0]/4.0
bggray=511

leftweightsvar=256.0
leftweightsmean=511.0

rightweightsvar=256.0
rightweightsmean=511.0

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
mymondleft=Mondrian(usingeizo=False, imagesize=[mondwidth, mondheight], encode=False, weights=leftweights)

bigarray[(monitorsize[1]/2.0)-mondheight/2.0:(monitorsize[1]/2.0)+mondheight/2.0,(monitorsize[0]/4.0)-mondwidth/2.0:(monitorsize[0]/4.0)+mondwidth/2.0] = mymondleft.mondrianarray

mymondright=Mondrian(usingeizo=False, imagesize=[mondwidth, mondheight], encode=False, weights=rightweights)

bigarray[(monitorsize[1]/2.0)-mondheight/2.0:(monitorsize[1]/2.0)+mondheight/2.0,(3*monitorsize[0]/4.0)-mondwidth/2.0:(3*monitorsize[0]/4.0)+mondwidth/2.0] = mymondright.mondrianarray

#Overlay transparent insets
bigarray[(monitorsize[1]/2.0)-(mondheight/4.0):(monitorsize[1]/2.0)+(mondheight/4.0),(3*monitorsize[0]/4.0)-(mondwidth/4.0):(3*monitorsize[0]/4.0)+(mondwidth/4.0)] -= 400


bigarray[bigarray>1023]=1023
bigarray[bigarray<0]=0

(N, M) = np.shape(bigarray)
newarray = np.zeros((N, M, 3), dtype=np.uint8)
newarray[:,:,0]=np.uint8(bigarray[:,:]/4)
newarray[:,:,1]=np.uint8(bigarray[:,:]/4)
newarray[:,:,2]=np.uint8(bigarray[:,:]/4)
pil_im = Image.fromarray(newarray)
pngfile="mondriantest"+time.strftime("%Y%m%d_%H%M")+".png"
pil_im.save(pngfile)
