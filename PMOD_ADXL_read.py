from math import ceil
import time 
from pynq import Xlnk
import numpy as np
import matplotlib.pyplot as plt
from pynq.lib import Pmod_ADC
from pynq.overlays.base import BaseOverlay

ol = BaseOverlay("base.bit")

adc = Pmod_ADC(ol.PMODB)


xlnk = Xlnk()

xlnk.cma_stats() 

#allocate a memory buffer 
px_buffer = xlnk.cma_array(shape=(100,), dtype=np.uint32)
py_buffer = xlnk.cma_array(shape=(100,), dtype=np.uint32)
pz_buffer = xlnk.cma_array(shape=(100,), dtype=np.uint32)


samples = []
count = 0
while count < 100:
    count = count +1
    #read x-value
    samplex = adc.read_raw(1,0,0)
    #time.sleep(0.01)
    #samples.append(sample[0])
    #read y-value
    sampley = adc.read_raw(0,1,0)
    time.sleep(0.01)
    #read z-value
    samplez = adc.read_raw(0,0,1)
    
    #populate the Xlnk buffers with the sample data
    px_buffer[count-1] = samplex[0]
    py_buffer[count-1] = sampley[0]
    pz_buffer[count-1] = samplez[0]
    
print("Xlnk buffer x-values: ",px_buffer)
print("Xlnk buffer y-values: ",py_buffer)
print("Xlnk buffer Z-values: ",pz_buffer)

adc.reset()