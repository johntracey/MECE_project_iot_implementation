from math import ceil
import time 
from pynq import Xlnk
import numpy as np
import matplotlib.pyplot as plt
from pynq.lib import Pmod_ADC
from pynq.overlays.base import BaseOverlay

ol = BaseOverlay("base.bit")
#create an instance of Xlnk 
xlnk = Xlnk()

xlnk.cma_stats() 

#allocate a memory buffer 
py_buffer = xlnk.cma_array(shape=(100,), dtype=np.uint32)

#allocate a output memory buffer
out_buffer = xlnk.cma_array(shape=(100,), dtype=np.uint32)

adc = Pmod_ADC(ol.PMODA)

#delay = 0.00
#values = np.linspace(0, 2, 20)
samples = []
count = 0
while count < 100:
    count = count +1
    sample = adc.read()
    #time.sleep(0.1)
    #samples.append(sample[0])
    py_buffer[count-1] = sample[0]
    
print("Xlnk buffer values: ",py_buffer)
    
    
    #print(samples[count])
    #print('Sample number: {:4.2f}\tSample read: {:4.2f}'.
          #format(count, sample[0], sample[0]))

time.sleep(5)

#Delete the base overlay
del ol

#Now load the streaming FIFO overlay to test sending the DATA from PS to PL via buffers

from pynq import Overlay
import pynq.lib.dma

#load the overlay built previously which contains a streaming FIFO
overlay = Overlay('/home/xilinx/pynq/overlays/basic_data_transfer_ps_pl/basic_data_transfer_ps_pl.bit')
#overlay?
#get full path to the fifo dma
#overlay.ip_dict 


dma = overlay.data_transfer.fifo_dma

print("input buffer values: ",py_buffer)
print("Output buffer values:",out_buffer)

dma.sendchannel.transfer(py_buffer)
dma.recvchannel.transfer(out_buffer)
print("Output Buffer Values after transfer: ",out_buffer)

time.sleep(5)
#Delete the streaming FIFO overlay
del overlay

#load the overlay for the custom streaming maths fucntion IP
overlay2 = Overlay('/home/xilinx/pynq/overlays/custom_streaming_function/custom_function.bit')
#overlay2?
#overlay2.ip_dict

dma2 = overlay2.simple_function.custom_dma
print("input buffer values: ",py_buffer)
print("Output buffer values:",out_buffer)

dma2.sendchannel.transfer(py_buffer)
dma2.recvchannel.transfer(out_buffer)

print("Output Buffer Values after transfer: ",out_buffer)

#pick out a number from the output buffer and convert to int for MQTT message
value = int(out_buffer[29])

#set up to publish some data using MQTT to a subscriber to the current topic: project/temp
import paho.mqtt.client as mqtt #import the client1
broker_address="192.168.0.33" #broker is running on the VM
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P2") #create new instance
print("connecting to broker")
client.connect(broker_address) #connect to broker
print("Publishing message to topic","project/temp")
print("buffer value # 29",out_buffer[29])
client.publish("project/temp",value)


#free the buffers
py_buffer.close()
out_buffer.close()