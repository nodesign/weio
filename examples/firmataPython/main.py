# This example is tested with SimpleDigitalFirmata sketch from Arduino. You can find this
# sketch inside Arduino, File > examples > firmata > SimpleDigitalFirmata
# It will blink Arduino's LED every second

from weioLib.weioUserApi import attach
import firmata

LED_PIN = 13

def setup():
    attach.process(arduino)
    
def arduino():
    a = firmata.Arduino("/dev/ttyACM2", 57600)
    print "Opened serial port for arduino"
    a.delay(2)
    a.pin_mode(LED_PIN, firmata.OUTPUT)
    while True :
        a.digital_write(LED_PIN, firmata.HIGH)
        print "LED is HIGH"
        a.delay(1)
        a.digital_write(LED_PIN, firmata.LOW)
        print "LED is LOW"
        a.delay(1)