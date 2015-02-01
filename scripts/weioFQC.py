#!/usr/bin/python -u
import sys, os, glob, logging, platform, json, signal, datetime
sys.path.append(os.getcwd())
from IoTPy.core.gpio import GPIO
from weioLib import weioGpio
from weioLib import weioRunnerGlobals
from weioLib import weioParser
from weioLib import weioUserApi
from weioLib import weioGpio
from weioLib import weioIO
from weioLib import weioConfig
from IoTPy.pyuper.utils import IoTPy_APIError, errmsg

import time

# This class detect if the LPC is shown on the USB bus
class Detector:
    def __init__(self, reset_pin=17, program_pin=22):
        reset_pin_str = str(reset_pin)
        program_pin_str = str(program_pin)
        self._gpio(reset_pin_str, "/sys/class/gpio/export")
        self._gpio(program_pin_str, "/sys/class/gpio/export")
        self._gpio("out","/sys/class/gpio/gpio"+reset_pin_str+"/direction")
        self._gpio("out","/sys/class/gpio/gpio"+program_pin_str+"/direction")
        self.uper_reset = "/sys/class/gpio/gpio"+reset_pin_str+"/value"
        self.uper_program = "/sys/class/gpio/gpio"+program_pin_str+"/value"

    def _gpio(self, content, file_name):
        try:
            file_id = os.open(file_name, os.O_WRONLY)
            os.write(file_id, content)
            os.close(file_id)
        except OSError:
            pass

    def _reset_uper(self):
        self._gpio("1",self.uper_reset)
        self._gpio("0",self.uper_reset)

    def detect(self):
        uper_flash_pattern = "CRP DISABLD"

        # put UPER in to programming mode
        self._gpio("1",self.uper_reset)
        self._gpio("1",self.uper_program)
        self._gpio("0",self.uper_reset)
        time.sleep(2) # wait for linux to settle after UPER reboot in to pgm state
        self._gpio("0",self.uper_program)

        # find UPER block device
        list_block_devs = glob.glob("/sys/block/sd*")
        block_device_name = ''
        header = ''
        for try_device_name in list_block_devs:
            try_device_name = "/dev/" + try_device_name.split('/')[-1]
            try:
                block_device = os.open(try_device_name, os.O_RDWR)
                os.lseek(block_device, 3 * 512, os.SEEK_SET)
                header = os.read(block_device,11)
                time.sleep(0.35) # reading can be slowww
                os.close(block_device)
            except OSError:
                pass
            if header == uper_flash_pattern: # "CRP DISABLD"
                block_device_name = try_device_name # found UPER
                break;
        if block_device_name == '':
            return 0

        # reset UPER
        self._reset_uper()
        time.sleep(.2)
        return 1
        
# This class will perform the test of all GPIOs
class GPIOTest:
    def __init__(self):
        self.g = weioGpio.WeioGpio()
        
        self.test_gpio()
        
        self.g.stop()
            
    def test_gpio(self):
        # Put all the GPIO to 1 via their pullup resistor
        # and control that they are read as 1
        for i in range(32):
            self.g.pinMode(i, GPIO.PULL_UP)
            a = self.g.digitalRead(i)
            if not a:
                print "Error : short with the ground on pin %d"%i
        
        # Put all the GPIO to 0 via their pulldown resistor
        # and control that they are read as 0
        for i in range(32):
            self.g.pinMode(i, GPIO.PULL_DOWN)
            # The RGB LED will give inacurate results here, so pin 18, 19 and 20 are skipped
            if not i in [18, 19, 20]: 
                a = self.g.digitalRead(i)
                if a:
                    print "Error : short with a supply on pin %d"%i
                
        # Turn all the GPIO, one by one, to 1 and control tht the other pins stays to 0
        for i in range(32):
            self.g.pinMode(i, GPIO.PULL_UP)
            for j in range(32):
                if not j in [i, 18, 19, 20]:
                    a = self.g.digitalRead(j)
                    if a:
                        print "Error : short between pin %d and %d" %(i, j)
            self.g.pinMode(i, GPIO.PULL_DOWN)

# This class will perform the test of all GPIOs
class testUI:
    def __init__(self, result):
        self.g = weioGpio.WeioGpio()
    
    def stop(self): 
        self.g.stop()
            
    def display_result(self):
        self.g.pinMode(19, GPIO.OUTPUT)
        self.g.digitalWrite(19, GPIO.LOW)
        time.sleep(.5)
        self.g.digitalWrite(19, GPIO.HIGH)
        time.sleep(.5)

if __name__ == "__main__":
    config = weioConfig.getConfiguration()                                             

    ### First test : Detect the LPC
    detect = Detector()
    res = detect.detect()
    time.sleep(3)

    if not res:
        print "LPC not found !"
        import ledBlink as led
        while config["first_time_run"] == "YES":    
            led.blink(.1)

    ### Second test : Test the GPIOs
    #gpio = GPIOTest()
