#!/usr/bin/env python
# encoding: utf-8

### 
#
# WEIO Web Of Things Platform
# Copyright (C) 2013 Nodesign.net, Uros PETREVSKI, Drasko DRASKOVIC
# All rights reserved
#
#               ##      ## ######## ####  #######  
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ######    ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#                ###  ###  ######## ####  #######
#
#                    Web Of Things Platform 
#
# This file is part of WEIO and is published under BSD license.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by the WeIO project.
# 4. Neither the name of the WeIO nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY WEIO PROJECT AUTHORS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL WEIO PROJECT AUTHORS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

__version__ = "0.02"

import struct, serial, threading, Queue, time, types, os, glob, urllib, urllib2

class Upgrader:
    def __init__(self):
        return

    def puttoFile(self, content, file_name):
        try:
            file_id = os.open(file_name, os.O_WRONLY)
            os.write(file_id, content)
            os.close(file_id)
        except OSError:
            pass

    def resetUper(self):
        self.puttoFile("1","/sys/class/gpio/gpio22/value")
        self.puttoFile("0","/sys/class/gpio/gpio22/value")

    def upgradeFirmware(self, fwUrl = "https://github.com/8devices/UPER/raw/master/dist/UPER-Release.bin"):
        acm_interface = "/dev/ttyACM0"
        sd_devices = "/dev/sd*"
        fw_file = "/tmp/latest_UPER_firmware.bin"
        UPER_flash_pattern = "CRP DISABLD"
        new_dev_list = []

        # put UPER1 in to programming mode
        self.puttoFile("22","/sys/class/gpio/export") # 14'th Carambola2 dev bord pin - reset on UPER
        self.puttoFile("23","/sys/class/gpio/export") # 15'th Carambola2 dev bord pin - prog on UPER
        self.puttoFile("out","/sys/class/gpio/gpio22/direction")
        self.puttoFile("out","/sys/class/gpio/gpio23/direction")
        self.puttoFile("1","/sys/class/gpio/gpio22/value")
        self.puttoFile("1","/sys/class/gpio/gpio23/value")
        self.puttoFile("0","/sys/class/gpio/gpio22/value")
        time.sleep(2) # wait for linux to settle after UPER reboot in to pgm state
        self.puttoFile("0","/sys/class/gpio/gpio23/value")

        # find UPER1 block device
        list_block_devs = glob.glob("/sys/block/sd*")
        block_device_name = ''
        for try_device_name in list_block_devs:
            try_device_name = "/dev/" + try_device_name.split('/')[-1]
            block_device = os.open(try_device_name, os.O_RDWR)
            os.lseek(block_device, 3 * 512, os.SEEK_SET)
            header = os.read(block_device,11)
            os.close(block_device)
            if header == UPER_flash_pattern: # "CRP DISABLD"
                #found UPER
                block_device_name = try_device_name
                break;
        if block_device_name == '':
            print "UPER firmware upgrade error, no UPPER board found"
            return

        # download firmware file 
        print fwUrl
        try:
            req = urllib2.Request(fwUrl)
            handle = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print "UPER: Can't download firmware, error code - %s." % e.code
            self.resetUper()
            return
        except urllib2.URLError:
            print "UPER: Bad URL for firmware file: %s" % fwUrl
            self.resetUper()
            return
        else:
            urllib.urlretrieve(fwUrl, fw_file + '.new')
            if os.path.isfile(fw_file + '.new'):
                os.rename(fw_file + '.new', fw_file)

        #os.system("dd if="+fw_file+" of="+new_dev_list[0]+" seek=4")

        # read the fw from file    
        fw_file_id = open(fw_file)
        firmware = fw_file_id.read()
        fw_file_id.close()

        block_device = os.open( block_device_name, os.O_RDWR)
        os.lseek(block_device, 4 * 512, os.SEEK_SET)
        os.write(block_device, firmware)
        os.close(block_device)

        # reset UPER
        self.resetUper()
        time.sleep(2)
        return

class Readers:
    def __init__(self, serial, outq, callback, decodefun):
        self.serial = serial
        self.outq = outq
        self.callback = callback
        self.alive = True
        # self.thread_read = threading.Thread(target=self.reader)
        #         self.thread_read.setDaemon(1)
        #         self.thread_read.start()
        #         self.decodefun = decodefun
        
    def reader(self):
        while self.alive:
            try:
                data = self.serial.read(1)            #read one, blocking
                n = self.serial.inWaiting()            #look if there is more
                if n:
                    data = data + self.serial.read(n)    #and get as much as possible
                if data:
                    if data[3] == '\x09':
                        interrupt = self.decodefun(data)
                        self.callback(interrupt)
                    else:
                        #print ":".join("{:02x}".format(ord(c)) for c in data)
                        self.outq.put(data)
            except RuntimeError:
                print "UPER API: serial port reading error!!!"
                break
        self.alive = False
    
    def stop(self):
        if self.alive:
            self.alive = False
            self.thread_read.join()

class UPER:       
    def stop(self):
        for i in range(7):
            self.detachInterrupt(i)
        self.reader.stop()
        self.ser.close()

    def encodeINT(self, intarg):
        if intarg < 64:
            return(chr(intarg))
        packedint = struct.pack( '>I', intarg ).lstrip('\x00')
        return(chr(0xc0 | (len(packedint) -1)) + packedint)

    def encodeBYTES(self, bytestr):
        if len( bytestr ) < 64:
            return (chr(0x40 | len(packedint)) + bytestr)
        packedlen = struct.pack( '>I', len(bytestr)).lstrip('\x00')
        if len(packedlen) == 1:
            return('\xc4'+packedlen+bytestr)
        elif len(pakedlen) == 2:
            return('\xc5' + packedlen + bytestr)
        else:
            print "UPER API: error - too long string"

    def encodeSFP(self, command, args):
        functions = { types.StringType : self.encodeBYTES, types.IntType : self.encodeINT }
        SFPcommand = chr(command) + ''.join(functions[ type(arg) ]( arg ) for arg in args)
        SFPcommand = '\xd4' + struct.pack('>H', len(SFPcommand)) + SFPcommand
        return(SFPcommand)

    def decodeSFP(self, buffer):
        result = []
        if buffer[0:1] != '\xd4':
            return( result )
        buflen = struct.unpack('>H', buffer[1:3])[0] + 3
        result.append( struct.unpack('b', buffer[3:4])[0] )
        pointer = 4
        args = []
        while pointer < buflen:
            argtype = ord(buffer[pointer:pointer+1])
            pointer +=1
            if argtype < 64:                    #short int
                args.append(argtype)
            elif argtype < 128:                    #short str
                arglen = argtype & 0x3f
                args.append(buffer[pointer:pointer+arglen])
                pointer += arglen
            else:
                arglen = argtype & 0x0f            #decoding integers
                if arglen == 0:
                    args.append(ord(buffer[pointer:pointer+1]))
                elif arglen == 1:
                    args.append(struct.unpack('>H', buffer[pointer:pointer+2])[0])
                elif arglen == 2:
                    args.append(struct.unpack('>I', '\x00' + buffer[pointer:pointer+3])[0])
                elif arglen == 3:
                    args.append(struct.unpack('>I', buffer[pointer:pointer+4])[0])
                pointer += arglen + 1

                if arglen == 4:
                    arglen = ord(buffer[pointer:pointer+1])
                    pointer += 1
                    args.append(buffer[pointer:pointer+arglen])
                    pointer += arglen
                elif arglen == 5:
                    arglen = struct.unpack('>H', buffer[pointer:pointer+2])[0]
                    pointer += 2
                    args.append(buffer[pointer:pointer+arglen])
                    pointer += arglen
        result.append(args)
        return(result)

    def UPER_IO(self, ret, buf):
        self.ser.write(buf)
        if ret == 0:
            return
        data = self.outq.get()
        return(data)

    def setPrimary(self, pinID):
        print "setPrimary", pinID 

    def setSecondary(self, pinID):
        print "setSecondary", pinID 

    def pinMode(self, pinID, pinMode):
        print "pinMode", pinID, " ", pinMode

    def digitalWrite(self, pinID, value):
        print "digitalWrite", pinID, " ", value

    def digitalRead(self, pinID):
        print "digitalRead", pinID

    def attachInterrupt(self, interruptID, pinID, mode):
        print "attachInterrupt", interruptID, " ", pinID, " ", mode
        
    def detachInterrupt(self, interruptID):
        print "detachInterrupt", interruptID
        
    def analogRead(self, analogPinID):
        print "analogRead", analogPinID
        
    def pwm0_begin(self, period):
        #print "pwm0_begin period:", period
        print "pwm0_begin", period
        
    def pwm1_begin(self, period):
        #print "pwm1_begin period:", period
        print "pwm1_begin", period
        
    def pwm0_set(self, channel, high_time):
        #print "pwm0_set high_time:", high_time
        print "pwm0_set", channel, " ", high_time
        
    def pwm1_set(self, channel, high_time):
        #print "pwm1_set high_time:", high_time
        print "pwm1_set", channel, " ", high_time
        
    def pwm0_end(self):
        print "pwm0_end"
        
    def pwm1_end(self):
        print "pwm1_end"
        
    def spi0_begin(self, divider, mode):
        print "spi0_begin"
        
    def spi0_trans(self, data, respond):
        print "spi0_trans"
        
    def spi0_end(self):
        self.UPER_IO(0, self.encodeSFP( 22, []))
         
    def i2c_begin(self):
        self.UPER_IO(0, self.encodeSFP(40, []))

    def i2c_trans(self, address, writeData, readLength):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(41, [address, writeData, readLength]))))

    def i2c_end(self):
        self.UPER_IO(0, self.encodeSFP( 42, []))

    def registerWrite(self, registerAddress, value):
        self.UPER_IO(0, self.encodeSFP(100, [registerAddress, value]))

    def registerRead(self, registerAddress):
        return(self.decodeSFP(self.UPER_IO(1, self.encodeSFP(101, [registerAddress])))[1][1])

    def getDeviceInfo(self):
        device_info = []
        result = self.decodeSFP(self.UPER_IO(1, self.encodeSFP(255, [])))
        if result[0] != -1:
            print "UPER error: getDeviceInfo wrong code."
            return
        result = result[1]
        if result[0] >> 24 != 0x55: # 0x55 == 'U'
            print "UPER error, getDeviceInfo unknown device/firmware type"
            return
        device_info.append("UPER") # type
        device_info.append((result[0] & 0x00ff0000) >> 16) #fw major
        device_info.append(result[0] & 0x0000ffff) #fw minor
        device_info.append(result[1]) # 16 bytes long unique ID from UPER CPU
        device_info.append(result[2]) # UPER LPC CPU part number
        device_info.append(result[3]) # UPER LPC CPU bootload code version
        return(device_info)

    def internalCallBack(intdata):
        #print"default CallBack is working %r" % intdata
        return

    def __init__(self, callbackfun = internalCallBack, serial_port = "/dev/ttyACM0"):
                # 
                # self.ser = serial.Serial(
                # port=serial_port,
                # baudrate=1, #virtual com port on USB is always max speed
                # parity=serial.PARITY_ODD,
                # stopbits=serial.STOPBITS_ONE,
                # bytesize=serial.EIGHTBITS,
                # timeout = 0.1
                # )
                # self.ser.flushInput()
        print "Uper created"
        self.outq = Queue.Queue()
        self.callbackfun = callbackfun
        self.reader = Readers(None, self.outq, self.callbackfun, self.decodeSFP)

if __name__ == '__main__':
    """
    print " Will init UPER1 and read ADC, upgrade firmware and read device info."
    u = UPER()
    u.setSecondary(30)
    print "analogRead = %x" % u.analogRead(3)
    u.stop()
    """
    #upgrader = Upgrader()
    #upgrader.upgradeFirmware()
    #del upgrader
    """
    uu = UPER()
    dev_info = uu.getDeviceInfo()
    print "%r" % dev_info
    uu.stop()
    """

