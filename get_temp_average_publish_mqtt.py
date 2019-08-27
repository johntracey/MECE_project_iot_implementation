#Sending data captured from the PS on the ZYNQ chip Temperature
#Collecting seven samples, sending the data to a custom IP on the PL to average the seven values
#Then send the result of the calculation back to the PS for printing
#Publish the data to the topic projec/temp using MQTT
#John Tracey DCU August 2019 MECE
 
from pynq import Overlay
overlay = Overlay('/home/xilinx/pynq/overlays/average/average.bit')

test_funct = overlay.average_0

import time
temp= [None] * 7 # temp array for 7 values
count = 0
while count < 7: # getting the cpu temp 7 times
    count = count +1
    with open('/sys/devices/soc0/amba/f8007100.adc/iio:device0/in_temp0_raw') as f: #open file to get cpu temp value
        for line in f:
            temp[count-1] = int(line) # populate the array with 7 sperate cpu temperature values
            print(temp[count-1])
            time.sleep(.005)
            
#write temperaturevalues to address 0x00 to 0x18 the values to registers a,b,c,d,e,f,g in programmable logic
test_funct.write(0x00, temp[0])
test_funct.write(0x04, temp[1])
test_funct.write(0x08, temp[2])
test_funct.write(0x0C, temp[3])
test_funct.write(0x10, temp[4])
test_funct.write(0x14, temp[5])
test_funct.write(0x18, temp[6])

#read from register h address 0x1C which should give the average of the 7 numbers sent to the IP
h = test_funct.read(0x1C)
print('The average value for CPU Temp is:', h)

#Set up the PYNQ as a MQTT publisher 
import paho.mqtt.client as mqtt #import the client1
broker_address="192.168.1.11" #broker is running on the VM
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P5") #create new instance
print("connecting to broker")
client.connect(broker_address) #connect to broker
print("Publishing message to topic","project/temp")
client.publish("project/temp",h,1)