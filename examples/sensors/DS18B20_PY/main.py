#######################################
#                                     #
#  USING A DS18B20 TEMPERATURE SENSO  #
#              WITH WEIO              #
#                                     #
#######################################
from weioLib.weio import *
 
from things.input.environmental.ds18b20 import DS18B20
 
def setup():
    attach.process(myProcess)
    
def myProcess():
 
    # Init the DS18B20 module
    sensors = DS18B20()
    
    # Get the sensors connected to WeIO
    sensorsList = sensors.getSensors()
    print sensorsList
    
    # Infinite loop
    while True:
        # For all sensors connected, get the temperature
        for sensor in sensorsList:
            print sensor, " : ", sensors.getTemperature(sensor)
        delay(5000)
