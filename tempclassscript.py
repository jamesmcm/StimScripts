from stimuliclass import *
linewidth=4
# stim=Lines(usingeizo=False, measuring=False, prefix=str(linewidth)+"distlines",
#         waittime=0.5, monitorsize=[1024,768], linewidth=linewidth, encode=False)
# #stim.run()

# stim=Cornsweet(usingeizo=False, measuring=False, prefix=str(linewidth)+"distlines", waittime=0.5, encode=False)

stim=WhiteIllusion(usingeizo=False, measuring=False, prefix=str(linewidth)+"distlines", waittime=0.5, encode=False, kind="gil")

# stim=Todorovic(usingeizo=False, measuring=False, prefix=str(linewidth)+"distlines", waittime=0.5, encode=False)

# stim=SinGrating(usingeizo=False, measuring=False, prefix=str(linewidth)+"distlines", waittime=0.5, encode=False, monitorsize=[1024,768])
