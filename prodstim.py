from stimuli import *
import numpy as np
import matplotlib.pyplot as ppl
import pylab
import eizoGS320


#nparray=cornsweet((3, 4), 512, 1,  mean_lum=511)
nparray= whites_illusion_bmcc((3, 4), 512, 1, 2, mean_lum=511,  start='high')
#ppl.imshow(nparray)
#pylab.show()

import Image
newarray=eizoGS320.encode_np_array(nparray)
#ppl.imshow(nparray)
#pylab.show()

pil_im = Image.fromarray(newarray)
pil_im.save("white1test.png")
